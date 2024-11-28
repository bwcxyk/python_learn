import os
import sys
import atexit
import datetime
from pyVmomi import vim
from pyVim.task import WaitForTask
from pyVim.connect import SmartConnect, Disconnect
from dotenv import load_dotenv

# 解析 .env 文件中的环境变量
load_dotenv()
host = os.getenv("VCENTER_HOST")
user = os.getenv("VCENTER_USERNAME")
password = os.getenv("VCENTER_PASSWORD")
vm_name = os.getenv("VM_NAME")


def connect():
    service_instance = None
    try:
        service_instance = SmartConnect(host=host, user=user, pwd=password, port=443, disableSslCertValidation=True)
        # doing this means you don't need to remember to disconnect your script/objects
        atexit.register(Disconnect, service_instance)
    except IOError as io_error:
        print(io_error)

    return service_instance


def search_for_obj(content, vim_type, name, folder=None, recurse=True):
    if folder is None:
        folder = content.rootFolder

    obj = None
    container = content.viewManager.CreateContainerView(folder, vim_type, recurse)

    for managed_object_ref in container.view:
        if managed_object_ref.name == name:
            obj = managed_object_ref
            break
    container.Destroy()
    return obj


def get_obj(content, vim_type, name, folder=None, recurse=True):
    obj = search_for_obj(content, vim_type, name, folder, recurse)
    if not obj:
        raise RuntimeError("Managed Object " + name + " not found.")
    return obj


def list_snapshots_recursively(snapshots):
    snapshot_data = []
    for snapshot in snapshots:
        snap_text = "Name: %s; Description: %s; CreateTime: %s; State: %s" % (
            snapshot.name, snapshot.description,
            snapshot.createTime, snapshot.state)
        snapshot_data.append(snap_text)
        snapshot_data = snapshot_data + list_snapshots_recursively(
            snapshot.childSnapshotList)
    return snapshot_data


def get_snapshots_by_name_recursively(snapshots, snapname):
    snap_obj = []
    for snapshot in snapshots:
        if snapshot.name == snapname:
            snap_obj.append(snapshot)
        else:
            snap_obj = snap_obj + get_snapshots_by_name_recursively(
                snapshot.childSnapshotList, snapname)
    return snap_obj


def get_current_snap_obj(snapshots, snapob):
    snap_obj = []
    for snapshot in snapshots:
        if snapshot.snapshot == snapob:
            snap_obj.append(snapshot)
        snap_obj = snap_obj + get_current_snap_obj(
            snapshot.childSnapshotList, snapob)
    return snap_obj


def manage_snapshots(vm, snapshot_operation):
    # 获取当前时间并格式化
    current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    snapshot_name = f"snapshot_{current_time}"
    if snapshot_operation != 'create' and vm.snapshot is None:
        print("Virtual Machine %s doesn't have any snapshots" % vm.name)
        sys.exit()

    if snapshot_operation == 'create':
        snapshot_name = snapshot_name
        description = "Auto create"
        dump_memory = False
        quiesce = False

        print("Creating snapshot %s for virtual machine %s" % (
            snapshot_name, vm.name))
        WaitForTask(vm.CreateSnapshot(
            snapshot_name, description, dump_memory, quiesce))

    elif snapshot_operation == 'remove':
        snapshot_name = 'snapshot_20240918_144111'
        snap_obj = get_snapshots_by_name_recursively(
            vm.snapshot.rootSnapshotList, snapshot_name)
        # if len(snap_obj) is 0; then no snapshots with specified name
        if len(snap_obj) == 1:
            snap_obj = snap_obj[0].snapshot
            print("Removing snapshot %s" % snapshot_name)
            WaitForTask(snap_obj.RemoveSnapshot_Task(True))
        else:
            print("No snapshots found with name: %s on VM: %s" % (
                snapshot_name, vm.name))

    elif snapshot_operation == 'list_all':
        print("Display list of snapshots on virtual machine %s" % vm.name)
        snapshot_paths = list_snapshots_recursively(
            vm.snapshot.rootSnapshotList)
        for snapshot in snapshot_paths:
            print(snapshot)

    elif snapshot_operation == 'list_current':
        current_snapref = vm.snapshot.currentSnapshot
        current_snap_obj = get_current_snap_obj(
            vm.snapshot.rootSnapshotList, current_snapref)
        current_snapshot = "Name: %s; Description: %s; " \
                           "CreateTime: %s; State: %s" % (
                               current_snap_obj[0].name,
                               current_snap_obj[0].description,
                               current_snap_obj[0].createTime,
                               current_snap_obj[0].state)
        print("Virtual machine %s current snapshot is:" % vm.name)
        print(current_snapshot)

    elif snapshot_operation == 'remove_all':
        print("Removing all snapshots for virtual machine %s" % vm.name)
        WaitForTask(vm.RemoveAllSnapshots())

    else:
        print("Specify operation in "
              "create/remove/list_all/list_current/remove_all")


def main():
    print("Trying to connect to VCENTER SERVER . . .")

    si = connect()

    print("Connected to VCENTER SERVER !")

    content = si.RetrieveContent()

    vm = get_obj(content, [vim.VirtualMachine], vm_name)

    manage_snapshots(vm, 'remove')


# Start program
if __name__ == "__main__":
    main()
