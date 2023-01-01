import unittest

from mock import patch

from lesspass.cli import parse_args


class TestParseArgs(unittest.TestCase):
    def test_parse_args_site(self):
        self.assertEqual(parse_args(["site"]).site, "site")

    def test_parse_args_login(self):
        self.assertEqual(parse_args(["site", "login"]).login, "login")

    def test_parse_args_LESSPASS_MASTER_PASSWORD_env_variable(self):
        with patch.dict("os.environ", {"LESSPASS_MASTER_PASSWORD": "password"}):
            self.assertEqual(parse_args([]).master_password, "password")

    def test_parse_args_master_password(self):
        self.assertEqual(
            parse_args(["site", "login", "masterpassword"]).master_password,
            "masterpassword",
        )

    def test_parse_args_l(self):
        self.assertTrue(parse_args(["site", "-l"]).l)
        self.assertTrue(parse_args(["site", "--lowercase"]).l)

    def test_parse_args_u(self):
        self.assertTrue(parse_args(["site", "-u"]).u)
        self.assertTrue(parse_args(["site", "--uppercase"]).u)

    def test_parse_args_d(self):
        self.assertTrue(parse_args(["site", "-d"]).d)
        self.assertTrue(parse_args(["site", "--digits"]).d)

    def test_parse_args_s(self):
        self.assertTrue(parse_args(["site", "-s"]).s)
        self.assertTrue(parse_args(["site", "--symbols"]).s)

    def test_parse_args_lu(self):
        args = parse_args(["site", "-lu"])
        self.assertTrue(args.l)
        self.assertTrue(args.u)
        self.assertFalse(args.d)
        self.assertFalse(args.s)

    def test_parse_args_lud(self):
        args = parse_args(["site", "-lud"])
        self.assertTrue(args.l)
        self.assertTrue(args.u)
        self.assertTrue(args.d)
        self.assertFalse(args.s)

    def test_parse_args_luds(self):
        args = parse_args(["site", "-luds"])
        self.assertTrue(args.l)
        self.assertTrue(args.u)
        self.assertTrue(args.d)
        self.assertTrue(args.s)

    def test_parse_args_no_lowercase(self):
        self.assertTrue(parse_args(["site", "--no-lowercase"]).nl)

    def test_parse_args_no_uppercase(self):
        self.assertTrue(parse_args(["site", "--no-uppercase"]).nu)

    def test_parse_args_no_digits(self):
        self.assertTrue(parse_args(["site", "--no-digits"]).nd)

    def test_parse_args_no_symbols(self):
        self.assertTrue(parse_args(["site", "--no-symbols"]).ns)

    def test_parse_args_length_default(self):
        self.assertEqual(parse_args(["site"]).length, 16)

    def test_parse_args_length_long(self):
        self.assertEqual(parse_args(["site", "--length", "8"]).length, 8)

    def test_parse_args_length_short(self):
        self.assertEqual(parse_args(["site", "-L6"]).length, 6)
        self.assertEqual(parse_args(["site", "-L", "12"]).length, 12)

    def test_parse_args_counter_default(self):
        self.assertEqual(parse_args(["site"]).counter, 1)

    def test_parse_args_counter_long(self):
        self.assertEqual(parse_args(["site", "--counter", "2"]).counter, 2)

    def test_parse_args_counter_short(self):
        self.assertEqual(parse_args(["site", "-C99"]).counter, 99)
        self.assertEqual(parse_args(["site", "-C", "100"]).counter, 100)

    def test_parse_args_clipboard_default(self):
        self.assertFalse(parse_args(["site"]).clipboard)

    def test_parse_args_clipboard_long(self):
        self.assertTrue(parse_args(["site", "--copy"]).clipboard)

    def test_parse_args_clipboard_short(self):
        self.assertTrue(parse_args(["site", "-c"]).clipboard)

    def test_parse_args_prompt_long(self):
        self.assertTrue(parse_args(["--prompt"]).prompt)

    def test_parse_args_prompt_short(self):
        self.assertTrue(parse_args(["-p"]).prompt)

    def test_parse_args_exclude_default(self):
        self.assertEqual(parse_args(["site"]).exclude, None)

    def test_parse_args_exclude(self):
        self.assertEqual(parse_args(["site", "--exclude", "!@$*+-"]).exclude, "!@$*+-")

    def test_parse_args_exclude_single_and_double_quote(self):
        self.assertEqual(parse_args(["site", "--exclude", "\"'"]).exclude, "\"'")

    def test_parse_no_fingerprint(self):
        self.assertTrue(parse_args(["site", "--no-fingerprint"]).no_fingerprint)
        self.assertFalse(parse_args(["site"]).no_fingerprint)

    def test_parse_args_save_path(self):
        self.assertEqual(
            parse_args(["--save", "/tmp/profiles.json"]).save_path, "/tmp/profiles.json"
        )
        self.assertEqual(parse_args(["site"]).save_path, None)
        with patch.dict("os.environ", {"XDG_CONFIG_HOME": "/tmp"}):
            self.assertEqual(
                parse_args(["--save"]).save_path, "/tmp/lesspass/profiles.json"
            )

    def test_parse_args_load_path(self):
        self.assertEqual(
            parse_args(["--load", "/tmp/profiles.json"]).load_path, "/tmp/profiles.json"
        )
        self.assertEqual(parse_args(["site"]).load_path, None)

    def test_parse_args_config_home_path(self):
        self.assertTrue(parse_args([]).config_home_path.endswith("/.config/lesspass"))

    def test_parse_args_XDG_CONFIG_HOME_env_variable(self):
        with patch.dict("os.environ", {"XDG_CONFIG_HOME": "/tmp"}):
            self.assertEqual(parse_args([]).config_home_path, "/tmp/lesspass")

    def test_parse_args_default_base_url(self):
        self.assertEqual(parse_args([]).url, "https://api.lesspass.com/")

    def test_parse_args_default_base_url(self):
        self.assertEqual(
            parse_args(["--url", "https://example.org/"]).url, "https://example.org/"
        )

    def test_nrt_parse_url_add_trailing_slash(self):
        self.assertEqual(
            parse_args(["--url", "https://example.org"]).url, "https://example.org/"
        )

    def test_export(self):
        self.assertEqual(
            parse_args(["--export", "/tmp/export.csv"]).export_file_path,
            "/tmp/export.csv",
        )

    def test_logout(self):
        self.assertTrue(parse_args(["--logout"]).logout)
