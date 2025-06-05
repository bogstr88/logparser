package main

import (
	"encoding/csv"
	"fmt"
	"os"
	"time"
)

const timeFormat = "15:04:05"

type Job struct {
	Description string
	Start       time.Time
	End         time.Time
	Duration    time.Duration
	PID         string
}

type StartOnlyJob struct {
	Description string
	Start       time.Time
	PID         string
}

func parseLog(filePath string) ([]Job, []StartOnlyJob, error) {
	file, err := os.Open(filePath)
	if err != nil {
		return nil, nil, err
	}
	defer file.Close()

	reader := csv.NewReader(file)
	records, err := reader.ReadAll()
	if err != nil {
		return nil, nil, err
	}

	jobs := make(map[string]struct {
		Description string
		Start       time.Time
	})
	var durations []Job
	var unmatchedStarts []StartOnlyJob

	for _, row := range records {
		if len(row) < 4 {
			continue
		}
		timestampStr := row[0]
		description := row[1]
		event := row[2]
		pid := row[3]

		timestamp, err := time.Parse(timeFormat, timestampStr)
		if err != nil {
			fmt.Printf("Invalid time format: %s\n", timestampStr)
			continue
		}

		switch event {
		case "START":
			jobs[pid] = struct {
				Description string
				Start       time.Time
			}{Description: description, Start: timestamp}
		case "END":
			if job, ok := jobs[pid]; ok {
				if timestamp.Before(job.Start) {
					fmt.Printf("ERROR - END time earlier than START time for PID %s: %s < %s\n",
						pid, timestamp.Format(timeFormat), job.Start.Format(timeFormat))
					continue
				}
				durations = append(durations, Job{
					Description: job.Description,
					PID:         pid,
					Start:       job.Start,
					End:         timestamp,
					Duration:    timestamp.Sub(job.Start),
				})
				delete(jobs, pid)
			} else {
				fmt.Printf("Unmatched END for PID %s at %s\n", pid, timestampStr)
			}
		}
	}

	for pid, info := range jobs {
		unmatchedStarts = append(unmatchedStarts, StartOnlyJob{
			Description: info.Description,
			PID:         pid,
			Start:       info.Start,
		})
	}

	return durations, unmatchedStarts, nil
}

func analyzeDurations(jobs []Job, unmatched []StartOnlyJob) {
	for _, job := range jobs {
		minutes := job.Duration.Minutes()
		status := ""
		if minutes > 10 {
			status = "ERROR"
		} else if minutes > 5 {
			status = "WARNING"
		}

		if status != "" {
			fmt.Printf("%s - ", status)
		}
		fmt.Printf("%s (PID %s) took %s from %s to %s\n",
			job.Description, job.PID, job.Duration,
			job.Start.Format(timeFormat), job.End.Format(timeFormat))
	}

	if len(unmatched) > 0 {
		fmt.Println("\n  Tasks that started but did not end:")
		for _, job := range unmatched {
			fmt.Printf("INCOMPLETE - %s (PID %s) started at %s\n",
				job.Description, job.PID, job.Start.Format(timeFormat))
		}
	}
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: go run script.go <log_file_path>")
		return
	}
	filePath := os.Args[1]

	durations, unmatched, err := parseLog(filePath)
	if err != nil {
		fmt.Printf("Error parsing log: %v\n", err)
		return
	}

	analyzeDurations(durations, unmatched)
}
