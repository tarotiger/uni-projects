# Testing Assumptions
- 'messages' data type has an additional key 'channel_id' to indicate which channel it was posted in
- 'messages' data type has an additional key 'react_id' which is a list and indicates what reacts have been performed on the post
- 'channels' data type has additional keys 'owner' and 'members' which indicate which users have special permissions as we can't determine how to assign user permissions otherwise
- user_profile_sethandle will allow two unique users to share a handle
- Users will be able to view all the information of other users' profiles (e.g. email)
- Users who post a message has permissions to delete their own messages 
- Given a token we can determine who the user is 
- Admins and owners both have the permission to pin a message
- Admins and owners are different for each channel
- The user who created the channel is the owner and the first user who joins after is an admin 
- 'permission_id' refers to the permission of the user in the slackr and not specific channels
- channel_listall will not list private channels you're not part of
- We cannot actually create automated tests for resetting one's password where a password is successfully reset - this has to be done manually, since the mail sending functionality is in server.py. Also, because the reset_code is randomly generated and not returned via the function (only sent to the email specified)  there's no way to grab it and use it while testing. Thus, we have not made tests for auth_passwordreset.py as the only thing we can test is if function "valid_password" in general.py works.

# Channel assumptions 
- Owners don't have special permissions unless they are in the channel 
- Admins and owners of slackr automatically become an owner of the channel when they are invited or when they join the channel 

# admin_userpermission_change
- An admin cannot make another user an owner 
- There has to be at least one owner of slackr 
- Users are able to change their permission_id as long as it's not giving them more permissions
- When a user gets their permission demoted, they still retain ownership to the channels they are currently in. (Admin/owners of slackr only get special permissions when they join a channel) 

# add_owner and remove_owner 
- An admin or owner of slackr can make any user an owner of a channel even if they (admin/owner) are not part of the channel

# userprofile_setname 
- When a user's name is changed, it is changed across all the channels they are currently in as well 

# search 
- When a user leaves a channel they can no longer search for the message they post 
- An empty string returns all the messages in every channel they are in

# Reacts
- valid react_id is assumed to be 1, since there is only one possible react in Slackr

# Scheduling Messages
- If a user is removed from a channel before their scheduled message is sent, the message still sends
- When testing message_sendlater, some of sendlater's functionality relies upon contacting the server and starting a serverside flask timer. This cannot be tested, so we are manually calling msg_sendlater_channel in order to make sure the actual functions are working. _In other words,_ we assumed that the timer function in server.py works.
