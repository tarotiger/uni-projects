COMP1531 Project User Assurance
======================================================================================
## Verification and Validiation 
Verification and validation are important aspects to consider when ensuring a system 
has been built correctly for the intended purpose.

### Verification
Verification refers to whether a system is free of bugs and does not have any
unexpected behaviour. For our implementation of the backend, we ensured that there 
were minimal bugs and our software behaved as expected by using some external
software tools such as:
    - pylint 
    - python3-coverage
    - advanced rest client 
    - pytest

#### Coverage
One of the most important tools was the python3-coverage, which measures how much of 
our code has been excecuted by our tests. Despite being a good tool to discover 
issues in the code such as infinite loops or redundent code, it does not necessarily 
equate to good test coverage. 

Overall, some of our functions could reach 100% coverage. This can be seen in 
message_react.py and message_unreact.py, which does not exist more than one valid 
react_id leaving some lines that checked for a valid react_id resulting in partial 
coverage. Other functions such as channel_removeowner and channel_leave have some 
partial coverage which contained for loops which ultiamtely break statements and exit prematurely. 

### Validation
Validation refers to satisfying our client's expectations. This could be done by 
executing our backend with Sally and Bob's frontend server and ensuring our functions 
match the expected behaviour of their implementation. 
However, in iteration2 since we were not required to have our backend working with the frontend, we used the user acceptance criteria to determine if we have satisfied the customer's need. 

#### User Acceptance Discussion

The following acceptance criteria was created after considering our client's requirements and reviewing Sally and Bob's frontend implementation. We chose to use rule-based acceptance criteria instead of scenario-based acceptance criteria as scenario-based user stories also tend to imply specific user actions, hence for our project, developing these types of user stories is more time consuming with less benefit to the validation of our implementation. Rule-based acceptance criteria are simpler to understand and can be applied to a wider variety of user stories. 



## User Acceptance Criteria
#### Epic: As a user, I would like to be able to authenticate my access to the service.

Story:
As a user I'd like to register an account so that I can use the service
- User is directed to a sign-up form once they press the button on the homepage
- The form contains four fields for the user to fill in:
	- Email
	- Password
	- First Name
	- Last Name
- Once filled in, they are registered as a valid user once they press the "Register" button
- The registered user is given a unique token which is allows them to log in

Story:
As a user I'd like to be able to log back in to Slackr so that I can resume using the service.
- User is directed to a log-in form once they press the button on the homepage
- When the user is logged in, they are given a unique token
- The form contains two fields - one for email and one for password
- If their details are correct, they are logged in once they press the "Log In" button

Story:
As a user, I'd like to reset my password so that I can still log in and message my group if I forget my password
- Reset password link is placed near the bottom of the login form
- User is prompted to enter their email
- An email is sent, containing a specific secret code 
- The user should be able to enter their new password into the interface, and when also provided with the secret code, successfully change their password.
- User is redirected to the login page afterwards

Story:
As a user, I'd like to I have my own profile, and thus others can clearly see who they're talking to in the channel.
- Each channel contains a list of members 
- If a user click on the name of a member, they will be directed to the following information about that user:
	- Email
	- First Name
	- Last Name
	- Slackr Handle
- If the user is not authenticated, they should be notified that this is the reason why they cannot view user profiles 


#### Epic: As a user, I would like to be able to use messages to communicate

Story:
As a member of a channel, I would like to send messages to my group so that we can communicate with each other
- The message field is placed at the bottom of the workspace
- The user should be able to type their message into the box
- The message sends when the user clicks the send button
- The user can't type more than 1000 characters
- Sent messages should appear in the channel's messages

Story:
As a user, I want to be able to send messages at specific times in the future, so that I can automatically contact team members.
- The message field is placed at the bottom of the workspace
- The user should be able to type their message into the box
- The user can't type more than 1000 characters
- Once the user clicks "send later", user is prompted with the option to set a date/time to send the message
- Message is sent when the indicated supplied time has been reached

Story:
As a member of a channel, I would like to edit my messages, so that messages remain relevant.
- The edit message option is on the right side of the sent message
- Clicking the edit message option prompts the user with a text field.
- The message can be saved by clicking the update changes button
- The message's text should be replaced with new message

Story:
As a member of a channel, I want to be able to delete my messages, so that other channel members only see relevant and useful messages.
- The delete message option is on the right side of the sent message
- The user is prompted with a popup to verify the action
- Message becomes deleted if user confirms the delete action
- Message no longer appears in the channel

Story:
As a member of a channel, I want to be able to pin my message, so that others can easily refer to the message.
- The message pin option is a dropdown option on the right side of each sent message. 
- The pin commences once the user clicks "pin to channel"
- The message is given special display treatment by the frontend 

Story:
As a member of a channel, I want to be able to unpin my message when they become irrelevant.
- The message unpin option is a dropdown option on the right side of the sent message
- The unpin commences once the user clicks "unpin from channel"
- The message's special mark is removed

Story:
As a member of a channel, I'd like react to a message, so that I don't have to respond with a new message.
- The react option is on the right side of the sent message
- User is prompted to try again if the react is invalid
- The default react should be a 'thumbs up'
- The message receives a react once the react option is clicked

Story:
As a member of a channel, I'd like un-react to a message, when they become irrelevant.
- The un-react option is on the right side of the sent message
- The react is removed once the user clicks the un-react option
- The user cannot unreact to a message they have not reacted to

#### Epic: As a user, I would like to have interact with channels.

Story:
As a user, I would like to create a public channel, so that any users can join.
- A user can create a channel by clicking the new channel option
- The user can must the channel a name by typing in the 'Channel Name' textbox
- The user can have the option to make the channel public
- Once the public channel is created, it can be searched by all other users

Story:
As an owner of a channel, I would like to create a private channel, so that public users are unable to join.
- A user can create a channel, to which they become the owner
- The user can must the channel a name by typing in the 'Channel Name' textbox
- The user can make the channel private
- Once the private channel is created, it cannot be searched by users who are not in the channel

Story:
As an owner or admin of a private channel, I would like to send invitations to users so that they can join my channel
- An owner of a private channel can add people to their channel
- The other users are added by entering their user id
- Once the user is invited, they are automatically added to the channel
- The added user can immediately view the channel which they could not previously view
- Admin/owners of Slackr can still join the private channel

Story:
As a user, I want to be able to see all the channels I am part of in a workspace.
- On the left side of the web server is a list of channels the user is in
- The user can click the channels to see messages and other channel details
- If the user leaves the channel, it is removed from the list

Story:
As a user, I would like to look for channels, so that I can join ones relevant to me
- A list of existing public channels exists on the left side of the webserver underneath the user's schannels
- The option to join the channel is displayed when the user clicks on the channel
- The user is immediately added to the channel after clicking the join button
- The user can now interact with the channel

Story:
As a member of a channel, I would like to be able to leave a channel when it no longer becomes relevant.
- User can click the channel leave button 
- The user's permissions are removed immediately
- The user can no longer view the channel's details

Story:
As an member of a channel, I'd like to be able to see who is in the channel.
- A list of members and owners is displayed at the top of the channel's details
- Members can click on the user's name to see their profile for more information
- Special icons indicate which members are owners

Story:
As an owner of a Slackr, I'd like to change owner permissions so that there is a workspace hierarchy.
- The owner of Slackr can change the permissions of the owner of a channel
- Owners can be removed/added by the Slackr owner
- They do not have to be part of the channel to implement these changes

Story:
As an owner of a channel, I want to be able to change the user permissions of certain group members.
- The owner can click the 'add owner' button to make a member another owner of the channel
- Owners can remove each others permissions and their own permissions

Story:
As a member of a channel, I want to be able to search for messages, so that I can find relevant information faster.
- A search bar should be available at the top of the page 
- The search should happen when the search button is clicked or the user presses enter
- Search returns the list of messages with a matching keyword

#### As user, I would like to hold team meetings
Story:
As a user, I would like to hold stand-ups within a channel to get daily updates on the team's progress.
- The standup acts as an online meeting on the channel
- The user can start a standup by sending '/standup' as a message
- The standup starts immediately and lasts for 15 mins
- All the messages are stored in a buffer and then sent once the standup ends