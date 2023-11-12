#!/bin/bash
counter=1
while true
 do
   endpoint="http://localhost:8080/"
   echo "[Request number: $((counter++))]: Performing a call to $endpoint"
   curl   -s -w "Response code: %{http_code}\n" "$endpoint"  -o /dev/null
   random_time_to_sleep=$(( $RANDOM % 10 ))
   echo "Sleeping for $random_time_to_sleep seconds"
   sleep "$random_time_to_sleep"
   echo "-----------------------"
done