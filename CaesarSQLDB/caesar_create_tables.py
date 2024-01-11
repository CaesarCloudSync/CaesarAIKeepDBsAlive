class CaesarCreateTables:
    def __init__(self) -> None:
        self.keepalivefields = ("firstname","lastname")

        

    def create(self,caesarcrud):
        caesarcrud.create_table("keepaliveid",self.keepalivefields,
        ("varchar(255) NOT NULL","varchar(255) NOT NULL"),
        "keepalive")


