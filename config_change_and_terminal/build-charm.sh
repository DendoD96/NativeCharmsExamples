cd simple_native_charm_vnf/charms/native-charm
if charmcraft build ; then
    find ./ -mindepth 1 ! -regex '^./build\(/.*\)?' -delete
    cp -r ./build/* ./
    rm -rf ./build
else
    echo "charmcraft build failed. The charm source code may not be present!"
fi