"""Prometheus queries"""

allowed_metrics_full_names = {
    "cpu_usage": "avg(irate(node_cpu_seconds_total{mode='user'}[1m])) * 100",  # Overall CPU usage (user mode)
    "memory_usage": "node_memory_MemTotal_bytes - (node_memory_Cached_bytes + node_memory_Buffers_bytes + node_memory_MemFree_bytes)",  # Overall memory usage
    "network_traffic": "irate(node_network_receive_bytes_total[1m]) + irate(node_network_transmit_bytes_total[1m])",  # Total network traffic (inbound + outbound)
    "io_activity": "irate(node_disk_read_bytes_total[1m]) + irate(node_disk_written_bytes_total[1m])",  # Total I/O activity (read + write)
}

full_metrics_full_names = {
    "cpu": {
        "cpu_usage": "avg(irate(node_cpu_seconds_total{mode='user'}[1m])) * 100",
        "node_scrape_collector_duration_seconds": "node_scrape_collector_duration_seconds",
        "node_procs_running": "node_procs_running",
        "node_procs_blocked": "node_procs_blocked",
        "node_entropy_available_bits": "node_entropy_available_bits",
        "node_load1": "node_load1",
        "node_load5": "node_load5",
        "node_load15": "node_load15",
        "pg_settings_random_page_cost": "pg_settings_random_page_cost",
        "pg_settings_max_worker_processes": "pg_settings_max_worker_processes",
        "pg_settings_max_parallel_workers": "pg_settings_max_parallel_workers",
        "pg_active_connection_count": "pg_stat_activity_count{state='active'} != 0",
    },
    "memory": {
        "memory_usage": "node_memory_MemTotal_bytes - (node_memory_Cached_bytes + node_memory_Buffers_bytes + node_memory_MemFree_bytes)",
        "node_memory_MemTotal_bytes": "node_memory_MemTotal_bytes",
        "node_memory_Cached_bytes": "node_memory_Cached_bytes",
        "node_memory_Buffers_bytes": "node_memory_Buffers_bytes",
        "node_memory_MemFree_bytes": "node_memory_MemFree_bytes",
        "node_memory_Inactive_anon_bytes": "node_memory_Inactive_anon_bytes",
        "node_memory_MemAvailable_bytes": "node_memory_MemAvailable_bytes",
        "node_memory_Dirty_bytes": "node_memory_Dirty_bytes",
        "pg_stat_activity_active_connections": "pg_stat_activity_count{state='active'} != 0",
        "pg_settings_shared_buffers_bytes": "pg_settings_shared_buffers_bytes",
        "pg_settings_effective_cache_size_bytes": "pg_settings_effective_cache_size_bytes",
        "pg_settings_maintenance_work_mem_bytes": "pg_settings_maintenance_work_mem_bytes",
        "pg_settings_work_mem_bytes": "pg_settings_work_mem_bytes",
        "pg_settings_max_wal_size_bytes": "pg_settings_max_wal_size_bytes",
        "pg_stat_bgwriter_buffers_alloc_rate": "irate(pg_stat_bgwriter_buffers_alloc[5m])",
        "pg_stat_bgwriter_buffers_backend_fsync_rate": "irate(pg_stat_bgwriter_buffers_backend_fsync[5m])",
        "pg_stat_bgwriter_buffers_checkpoint_rate": "irate(pg_stat_bgwriter_buffers_checkpoint[5m])",
        "pg_stat_bgwriter_buffers_clean_rate": "irate(pg_stat_bgwriter_buffers_clean[5m])",
        "pg_stat_database_conflicts_rate": "irate(pg_stat_database_conflicts[5m])",
        "pg_stat_database_deadlocks_rate": "irate(pg_stat_database_deadlocks[5m])",
    },
    "network": {
        "node_sockstat_tcp_time_wait": "node_sockstat_TCP_tw",
        "node_sockstat_tcp_orphan": "node_sockstat_TCP_orphan",
        "node_sockstat_tcp_alloc": "node_sockstat_TCP_alloc",
        "node_sockstat_tcp_inuse": "node_sockstat_TCP_inuse",
        "node_netstat_tcp_passive_opens_rate": "irate(node_netstat_Tcp_PassiveOpens[1m])",
        "pg_stat_activity_active_connections": "pg_stat_activity_count{state='active'} != 0",
    },
    "io": {
        "pg_stat_database_tup_fetched_total": "SUM(pg_stat_database_tup_fetched)",
        "pg_stat_database_tup_inserted_total": "SUM(pg_stat_database_tup_inserted)",
        "pg_stat_database_tup_updated_total": "SUM(pg_stat_database_tup_updated)",
        "process_open_file_descriptors": "process_open_fds",
        "pg_stat_database_xact_commit_rate": "irate(pg_stat_database_xact_commit[5m])",
        "pg_stat_database_xact_rollback_rate": "irate(pg_stat_database_xact_rollback[5m])",
        "pg_stat_database_tup_updated_non_zero": "pg_stat_database_tup_updated != 0",
        "pg_stat_database_blks_hit_ratio": "pg_stat_database_blks_hit / (pg_stat_database_blks_read + pg_stat_database_blks_hit)",
        "pg_stat_database_temp_bytes_rate": "irate(pg_stat_database_temp_bytes[5m])",
        "pg_stat_bgwriter_checkpoint_write_time_rate": "irate(pg_stat_bgwriter_checkpoint_write_time[5m])",
        "pg_stat_bgwriter_checkpoint_sync_time_rate": "irate(pg_stat_bgwriter_checkpoint_sync_time[5m])",
        "node_filesystem_used_bytes": "node_filesystem_size_bytes - node_filesystem_avail_bytes",
        "node_filesystem_size_bytes": "node_filesystem_size_bytes",
        "node_filesystem_used_ratio": "1 - (node_filesystem_free_bytes / node_filesystem_size_bytes)",
        "node_disk_reads_completed_rate": "irate(node_disk_reads_completed_total[1m])",
        "node_disk_writes_completed_rate": "irate(node_disk_writes_completed_total[1m])",
        "node_disk_io_in_progress": "node_disk_io_now",
        "node_disk_read_bytes_rate": "irate(node_disk_read_bytes_total[1m])",
        "node_disk_written_bytes_rate": "irate(node_disk_written_bytes_total[1m])",
        "node_disk_io_time_seconds_rate": "irate(node_disk_io_time_seconds_total[1m])",
        "node_disk_io_time_weighted_seconds_rate": "irate(node_disk_io_time_weighted_seconds_total[1m])",
        "node_disk_read_time_seconds_rate": "irate(node_disk_read_time_seconds_total[1m])",
        "node_disk_write_time_seconds_rate": "irate(node_disk_write_time_seconds_total[1m])",
        # "node_disk_io_time_seconds_rate": "irate(node_disk_io_time_seconds_total[1m])"
    },
}
