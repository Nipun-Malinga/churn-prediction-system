interface ScheduleInterval {
  value: string;
}

interface DagData {
  dag_display_name: string;
  dag_id: string;
  description: string | null;
  is_active: boolean;
  is_paused: boolean;
  last_parsed_time: string;
  next_dagrun: string;
  schedule_interval: ScheduleInterval;
}

interface DagDetails {
  dags: DagData[];
}

export type { DagData, DagDetails };
