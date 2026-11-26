# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "ceca31d0-c4b0-40a5-a1ed-4ef21beef54d",
# META       "default_lakehouse_name": "Final_lakehouse",
# META       "default_lakehouse_workspace_id": "8cfb619c-2004-4b43-98b3-42cf839fb476",
# META       "known_lakehouses": [
# META         {
# META           "id": "ceca31d0-c4b0-40a5-a1ed-4ef21beef54d"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************


# ============================================================
# NB_11_EXECUTION_HISTORY_UPDATE
# ============================================================

# Parameter cell
exec_seq = 0
run_id = ""

from pyspark.sql import functions as F
from delta.tables import DeltaTable
from datetime import datetime, timezone

print("Execution History Update initialized")


# ============================================================
# 1. VALIDATE PARAMETERS
# ============================================================

if exec_seq is None or int(exec_seq) <= 0:
    raise ValueError("Invalid execution sequence")

if run_id is None or not str(run_id).strip():
    raise ValueError("Invalid run ID")

exec_seq = int(exec_seq)
run_id = str(run_id)

print("Execution Sequence:", exec_seq)
print("Run ID:", run_id)


# ============================================================
# 2. VERIFY RUNNING EXECUTION RECORD
# ============================================================

execution_record = (
    spark.table("control_execution_log")
    .filter(
        (F.col("exec_seq") == exec_seq) &
        (F.col("run_id") == run_id)
    )
)

if execution_record.count() != 1:
    raise ValueError("Matching execution record not found")

current_status = execution_record.first()["execution_status"]

if current_status != "RUNNING":
    raise ValueError(
        f"Expected RUNNING status, found {current_status}"
    )

print("RUNNING execution record verified")


# ============================================================
# 3. READ GOLD AUDIT SUMMARY
# ============================================================

gold_audit = spark.table("gold_control_audit_summary")

required_columns = [
    "exec_seq",
    "run_id",
    "audit_stage",
    "source_table",
    "metric_name",
    "metric_value",
    "audit_timestamp"
]

missing_columns = [
    column for column in required_columns
    if column not in gold_audit.columns
]

if missing_columns:
    raise ValueError(
        f"Missing audit columns: {missing_columns}"
    )

gold_audit = gold_audit.select(*required_columns)

audit_mismatch = gold_audit.filter(
    (F.col("exec_seq") != exec_seq) |
    (F.col("run_id") != run_id)
).limit(1).count()

if audit_mismatch > 0:
    raise ValueError(
        "Gold audit summary execution metadata mismatch"
    )

audit_count = gold_audit.count()

if audit_count == 0:
    raise ValueError("No audit metrics available")

print("Gold audit metrics:", audit_count)


# ============================================================
# 4. CHECK FOR EXISTING HISTORY
# ============================================================

history_table = spark.table("control_execution_summary")

existing_count = (
    history_table
    .filter(
        (F.col("exec_seq") == exec_seq) &
        (F.col("run_id") == run_id)
    )
    .count()
)

if existing_count > 0:

    raise ValueError(
        "Execution history already exists for this run. "
        "Duplicate insertion prevented."
    )


# ============================================================
# 5. APPEND EXECUTION SUMMARY
# ============================================================

history_to_append = gold_audit.select(
    F.col("exec_seq").cast("long").alias("exec_seq"),
    F.col("run_id").cast("string").alias("run_id"),
    F.col("audit_stage"),
    F.col("source_table"),
    F.col("metric_name"),
    F.col("metric_value").cast("string").alias("metric_value"),
    F.col("audit_timestamp")
)

(
    history_to_append.write
    .format("delta")
    .mode("append")
    .saveAsTable("control_execution_summary")
)

print("Execution history appended successfully")


# ============================================================
# 6. VERIFY SAVED HISTORY
# ============================================================

saved_history_count = (
    spark.table("control_execution_summary")
    .filter(
        (F.col("exec_seq") == exec_seq) &
        (F.col("run_id") == run_id)
    )
    .count()
)

if saved_history_count != audit_count:
    raise ValueError(
        f"History count mismatch. Expected {audit_count}, "
        f"found {saved_history_count}"
    )

print("History count verified:", saved_history_count)


# ============================================================
# 7. UPDATE EXECUTION STATUS TO SUCCESS
# ============================================================

execution_delta = DeltaTable.forName(
    spark,
    "control_execution_log"
)

execution_delta.update(
    condition=(
        (F.col("exec_seq") == exec_seq) &
        (F.col("run_id") == run_id) &
        (F.col("execution_status") == "RUNNING")
    ),
    set={
        "end_timestamp": F.current_timestamp(),
        "execution_status": F.lit("SUCCESS"),
        "error_message": F.lit(None).cast("string")
    }
)

# Verify the update
final_record = (
    spark.table("control_execution_log")
    .filter(
        (F.col("exec_seq") == exec_seq) &
        (F.col("run_id") == run_id)
    )
    .first()
)

if final_record["execution_status"] != "SUCCESS":
    raise ValueError("Failed to update execution status to SUCCESS")

print("Execution completed successfully")


# ============================================================
# 8. DISPLAY EXECUTION HISTORY
# ============================================================

display(
    spark.table("control_execution_log")
    .filter(
        (F.col("exec_seq") == exec_seq) &
        (F.col("run_id") == run_id)
    )
)

display(
    spark.table("control_execution_summary")
    .filter(
        (F.col("exec_seq") == exec_seq) &
        (F.col("run_id") == run_id)
    )
    .orderBy("audit_stage", "source_table", "metric_name")
)


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
