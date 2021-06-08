-- :name get_user :one
-- :doc duplicate names
select * from users where user_id = %(user_id)s

-- :name get_user :one
-- :doc duplicate names
select * from users where user_id = %(user_id)s

-- :many
-- :doc no name
select * from users where username like %(pattern)s

-- :many :name search_users :many
-- :doc duplicate options
select * from users where username like %(pattern)s

-- :name update_username :affected
-- :doc unknown option
update users set username = %(username)s where user_id = %(user_id)s

-- :name save_user :void
insert into users (
    username,
    firstname,
    lastname,
    email,
    created
) values %s;

-- :template save_user
(%(username)s, %(firstname)s, %(lastname)s, %(email)s, now())

-- :template save_user
(%(username)s, %(firstname)s, %(lastname)s, %(email)s, now())

-- :name get_username :scalar :one
-- :doc multiple return types
select username from users where user_id = %(user_id)s

-- :name save_users :void :execute many
-- :doc unknown execute value
insert into users (username, firstname, lastname, email, created) values %s

-- :name find_users :many
-- :doc no sql
