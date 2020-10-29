#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/chadchiang/turtle_ws/src/turtlebot3/turtlebot3_example"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/chadchiang/turtle_ws/install/lib/python2.7/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/chadchiang/turtle_ws/install/lib/python2.7/dist-packages:/home/chadchiang/turtle_ws/build/lib/python2.7/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/chadchiang/turtle_ws/build" \
    "/usr/bin/python2" \
    "/home/chadchiang/turtle_ws/src/turtlebot3/turtlebot3_example/setup.py" \
    build --build-base "/home/chadchiang/turtle_ws/build/turtlebot3/turtlebot3_example" \
    install \
    --root="${DESTDIR-/}" \
    --install-layout=deb --prefix="/home/chadchiang/turtle_ws/install" --install-scripts="/home/chadchiang/turtle_ws/install/bin"
