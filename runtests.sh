#!/bin/bash
for test in `ls Tests/*.py`; do
    echo '***' $test '***'
    python $test
    if [ $? -ne 0 ]; then
        echo Error in $test
        exit $?
    fi
done
