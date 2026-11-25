def test_pwd(node_0):
    exit_code, out, err = node_0.files.pwd()
    assert exit_code == 0, f"Ошибка: pwd вернул код {exit_code}: {err}"
    assert out.strip().startswith("/"), f"Ошибка: неожиданный путь {out.strip()}"

def test_create_file(node_0):
    exit_code, out, err = node_0.files.touch("test_file")
    assert exit_code == 0, f"Ошибка: pwd вернул код {exit_code}: {err}"
    exit_code, out, err = node_0.command("ls -la")
    assert exit_code == 0, f"Ошибка: pwd вернул код {exit_code}: {err}"
    exit_code, out, err = node_0.files.cat("test_file")
    assert exit_code == 0, f"Ошибка: pwd вернул код {exit_code}: {err}"
    assert out.strip() == "", f"Ошибка: файл не пустой, получено: {out!r}"
    exit_code, out, err = node_0.command("rm test_file")
    assert exit_code == 0, f"Ошибка: pwd вернул код {exit_code}: {err}"
    exit_code, out, err = node_0.command("ls -la")
    assert exit_code == 0, f"Ошибка: pwd вернул код {exit_code}: {err}"


def test_reconnect_keeps_working(node_0):
    ec, out, _ = node_0.command("id")
    assert ec == 0

    node_0._base.ssh.close()
    node_0._base.ssh.reconnect()

    ec, out, _ = node_0.command("id")
    assert ec == 0, f"После reconnect нода не отвечает: {out}"
    print("\n[OK] reconnect: соединение снова рабочее")


def test_reboot_and_reconnect(node_0):
    ec, boot_id_before, err = node_0.files.cat("/proc/sys/kernel/random/boot_id")
    assert ec == 0, f"Не удалось прочитать boot_id до reboot: {err}"
    boot_id_before = boot_id_before.strip()
    print(f"\n[1] boot_id до reboot: {boot_id_before}")

    node_0.reboot()

    ec, out, _ = node_0.command("id")
    assert ec == 0, f"После reboot нода не отвечает: {out}"
    print(f"[2] После reboot: {out.strip()}")

    ec, boot_id_after, err = node_0.files.cat("/proc/sys/kernel/random/boot_id")
    assert ec == 0, f"Не удалось прочитать boot_id после reboot: {err}"
    boot_id_after = boot_id_after.strip()
    print(f"[3] boot_id после reboot: {boot_id_after}")

    assert boot_id_after != boot_id_before, (
        f"Нода НЕ перезагрузилась: boot_id не изменился ({boot_id_before})"
    )
    print("[OK] boot_id изменился, перезагрузка реально произошла")