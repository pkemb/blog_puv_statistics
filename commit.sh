#!/bin/bash

current_year=$(date +"%Y")
stat_file="page_puv_statistics_${current_year}.json"
if [ -f "$stat_file" ]; then
    commit_msg=$(cat $stat_file | tr '[,{}]' '\n' | grep time | cut -d"\"" -f4 | sort -n | tail -n1)
else
    commit_msg=$(date +"%Y-%m-%d %H:%M:%S")
fi

git add -A
git commit --allow-empty -m "date: $commit_msg"
git push origin master