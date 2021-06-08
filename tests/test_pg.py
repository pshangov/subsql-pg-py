import pytest

from subsql_pg import pgdriver, PgCommand 
from subsql.parser import ParserError

def test_commands():
    path = './res/fixtures/commands.sql'
    errors, commands = pgdriver.parse(path)

    assert len(errors) == 0
    assert len(commands) == 7

    assert type(commands[0]) == PgCommand
    assert commands[0].name == 'user_for_id'
    assert commands[0].query == 'select * from users where user_id = %(user_id)s;'
    assert commands[0].returns == 'one'
    assert commands[0].execute == None

    assert type(commands[1]) == PgCommand
    assert commands[1].name == 'search_users'
    assert commands[1].query == 'select * from users where username like %(pattern)s;'
    assert commands[1].returns == 'many'
    assert commands[1].execute == None

    assert type(commands[2]) == PgCommand
    assert commands[2].name == 'update_username'
    assert commands[2].query == 'update users set username = %(username)s\nwhere user_id = %(user_id)s;'
    assert commands[2].returns == 'rowcount'
    assert commands[2].execute == None

    assert type(commands[3]) == PgCommand
    assert commands[3].name == 'get_username'
    assert commands[3].query == 'select username from users where user_id = %(user_id)s;'
    assert commands[3].returns == 'scalar'
    assert commands[3].execute == None

    assert type(commands[4]) == PgCommand
    assert commands[4].name == 'add_user'
    assert commands[4].query == 'insert into users (username) values (%(username)s);'
    assert commands[4].returns == 'lastrowid'
    assert commands[4].execute == None

    assert type(commands[5]) == PgCommand
    assert commands[5].name == 'save_user'
    assert commands[5].query == 'insert into users (\n    username,\n    firstname,\n    lastname,\n    email,\n    created\n) values %s;'
    assert commands[5].returns == 'void'
    assert commands[5].execute == 'values'
    assert commands[5].template == '(%(username)s, %(firstname)s, %(lastname)s, %(email)s, now())'

    assert type(commands[6]) == PgCommand
    assert commands[6].name == 'set_created'
    assert commands[6].returns == 'void'
    assert commands[6].execute == None

def test_errors():
    path = './res/fixtures/errors.sql'
    errors, commands = pgdriver.parse(path)

    assert len(errors) == 9
    assert len(commands) == 1

    assert type(commands[0]) == PgCommand
    assert commands[0].name == 'get_user'
    assert commands[0].query == 'select * from users where user_id = %(user_id)s'
    assert commands[0].returns == 'one'
    assert commands[0].execute == None

    assert type(errors[0]) == ParserError
    assert errors[0].message == "Command get_user already exists"
    assert errors[0].file == './res/fixtures/errors.sql'
    assert errors[0].lineno == 5

    assert type(errors[1]) == ParserError
    assert errors[1].message == "Snippet doesn't have a name"
    assert errors[1].file == './res/fixtures/errors.sql'
    assert errors[1].lineno == 9

    assert type(errors[2]) == ParserError
    assert errors[2].message == "Template save_user already exists"
    assert errors[2].file == './res/fixtures/errors.sql'
    assert errors[2].lineno == 33

    assert type(errors[3]) == ParserError
    assert errors[3].message == "Function for template save_user must have ':execute values' specified"
    assert errors[3].file == './res/fixtures/errors.sql'
    assert errors[3].lineno == 30

    assert type(errors[4]) == ParserError
    assert errors[4].message == "Found duplicate option many"
    assert errors[4].file == './res/fixtures/errors.sql'
    assert errors[4].lineno == 13

    assert type(errors[5]) == ParserError
    assert errors[5].message == "Unsupported option affected"
    assert errors[5].file == './res/fixtures/errors.sql'
    assert errors[5].lineno == 17

    assert type(errors[6]) == ParserError
    assert errors[6].message == "Multiple returns types (scalar, one) specified for command get_username"
    assert errors[6].file == './res/fixtures/errors.sql'
    assert errors[6].lineno == 36

    assert type(errors[7]) == ParserError
    assert errors[7].message == "Parameter to :execute must be 'batch' or 'values', not 'many'"
    assert errors[7].file == './res/fixtures/errors.sql'
    assert errors[7].lineno == 40

    assert type(errors[8]) == ParserError
    assert errors[8].message == "No query found for command find_users"
    assert errors[8].file == './res/fixtures/errors.sql'
    assert errors[8].lineno == 44

