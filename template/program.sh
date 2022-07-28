if [ $# -lt 1 ]; then
    echo "Usage: $0 [<args>]"
    exit 1
else
    while getopts ":a:pso" opt; do
        case $opt in
            a)
                echo "$OPTARG"
                ;;
            s)
                sleep 3
                ;;
            o)
                sleep 1
                ;;
            p)
                echo 42 && exit 42
                ;;
            \?)
                echo "Invalid option: -$OPTARG" >&2
                exit 1
                ;;
            :)
                echo "Option -$OPTARG requires an argument." >&2
                exit 1
                ;;
        esac
    done 
fi
