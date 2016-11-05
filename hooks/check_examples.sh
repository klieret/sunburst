cd ../examples
pwd
ls
. ./setup_path.sh
for file in *.py
do
    echo $file
    python3 $file
done

