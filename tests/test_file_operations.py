def md5_of(node, path):
    ec, out, err = node.checks.md5sum(path)
    assert ec == 0, f"md5sum не сработал для {path}: {err}"
    return out.split()[0]


def _mpath_device(node):
    ec, out, err = node.disks.prepare_multipath()
    assert ec == 0, f"prepare_multipath не сработал: {err}"
    name = node.disks.get_mpath_device(out)
    return f"/dev/mapper/{name}"


def test_file_operations(initiator, disk):
    node = initiator
    use_disk = disk
    mnt = "/mnt/miniikea"

    ec, _, err = node.files.touch("/root/test_file.txt")
    assert ec == 0, f"touch упал: {err}"

    ec, out, err = node.files.cat("/root/test_file.txt")
    assert ec == 0, f"cat упал: {err}"
    assert out.strip() == "", f"файл не пустой: {out!r}"

    text = "Hello IKEA"
    ec, _, err = node.files.echo(text, "/root/test_file.txt")
    assert ec == 0, f"echo упал: {err}"

    ec, out, err = node.files.cat("/root/test_file.txt")
    assert ec == 0, f"cat упал: {err}"
    assert text in out, f"текст не записался: {out!r}"

    ec, _, err = node.files.mkdir("/root/backup")
    assert ec == 0, f"mkdir упал: {err}"
    ec, _, err = node.files.cp("/root/test_file.txt", "/root/backup/test_file.txt")
    assert ec == 0, f"cp упал: {err}"
    assert md5_of(node, "/root/test_file.txt") == md5_of(node, "/root/backup/test_file.txt")

    if use_disk:
        ec, out, err = node.disks.lsblk()
        assert ec == 0, f"lsblk упал: {err}"
        print("\nlsblk:\n", out)

        dev = _mpath_device(node)
        print(f"Монтируем диск: {dev}")

        ec, _, err = node.disks.mkfs("ext4", dev)
        assert ec == 0, f"mkfs упал: {err}"

        node.files.mkdir(mnt)
        ec, _, err = node.disks.mount(dev, mnt)
        assert ec == 0, f"mount упал: {err}"

        try:
            node.files.cp("/root/test_file.txt", f"{mnt}/test_file.txt")
            assert md5_of(node, "/root/test_file.txt") == md5_of(node, f"{mnt}/test_file.txt")
            hash_on_disk = md5_of(node, f"{mnt}/test_file.txt")
        finally:
            node.disks.umount(mnt)

    node.reboot()

    if use_disk:
        dev = _mpath_device(node)
        node.files.mkdir(mnt)
        ec, _, err = node.disks.mount(dev, mnt)
        assert ec == 0, f"mount после reboot упал: {err}"
        try:
            assert md5_of(node, f"{mnt}/test_file.txt") == hash_on_disk, \
                "файл испортился после reboot"
        finally:
            node.disks.umount(mnt)

    node.command("rm -rf /root/backup /root/test_file.txt")