#!/bin/bash
cd /Users/cwconlon/@dev/mlb
chmod +x *.sh                    # one-time, if not already executable
mkdir -p bin
ln -s ../rup_run_stage.sh bin/roster_stage
ln -s ../rup_run_stage_ls.sh bin/roster_stage_list
ln -s ../rup_run_load.sh bin/roster_load
ln -s ../rup_run_load_ls.sh bin/roster_load_list
ln -s ../rup_ls.sh bin/roster_run_result