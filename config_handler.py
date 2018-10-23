import configparser


class ConfigHandler():
    def __init__(self, config_path):
        self.config_path = config_path
        self.con = configparser.ConfigParser()
        self.con.read(config_path)

    def read_one_section(self, section):
        if not self.con.has_section(section):
            return None
        return self.con.items(section)

    def section_is_exist(self, section):
        return section in self.con.sections()

    def add_or_update_one_section(self, section, key_value_list):
        """
        the existed key-values will be overwrite!!!
        :param section:
        :param key_value_list: list, like [('ff', '13212123'), ('gg', '4564564646')]
        :return:
        """
        if not self.section_is_exist(section):
            self.con.add_section(section)
        for k, v in key_value_list:
            self.con.set(section, k, v)
        self._save_config()

    def remove_section(self, section):
        if not self.section_is_exist(section):
            return True
        self.con.remove_section(section)
        self._save_config()
        return True

    def remove_option(self,section, key):
        """
        :param section:
        :param key_value:  key, string, like 'gg',
        :return:
        """
        self.con.remove_option(section,key)
        if not self.con.options(section):  # option is none, drop the section.
            self.remove_section(section)
        self._save_config()

    def _save_config(self):
        with open(self.config_path,'w',encoding='utf-8') as f:
            self.con.write(f)


if __name__ == '__main__':
    c = ConfigHandler('selenium_identify.conf')
    print(c.read_one_section('123'))
    print(c.section_is_exist('1'))
    print(c.add_or_update_one_section('1',[('g','f')]))
    # print(c.remove_section('1'))
    print(c.remove_option('1','g'))
    print(c.section_is_exist('1'))




