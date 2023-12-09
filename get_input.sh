my_cookie=$(cat ./cookie.txt)
echo $my_cookie

#url_path_str=$(awk -F/ '{x=$(NF)+0;print $(NF-1) " " x}' <(echo $PWD))
year=2023
day=$1
curYear=$(date +%Y)
if [[ "$day" -ge "1" ]] && [[ "$day" -le "25" ]]
then
    if [[ "$year" -ge "2015" ]] && [[ "$year" -le "$curYear" ]]
    then
        urlPath="https://adventofcode.com/$year/day/$day/input"
        echo $urlPath >&2
        file_name="./data/day${day}_input.txt"
        curl "$urlPath" -H "$my_cookie" -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36' --compressed > $file_name
        cat $file_name
    else
        echo "Your dirPath doesn't match a year. CWD must be end with year/day" >&2
    fi
else
    echo "Your dirPath doesn't match a year. CWD must be end with year/day" >&2
fi

