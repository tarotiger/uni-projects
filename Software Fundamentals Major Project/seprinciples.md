# Software Engineering Principles

## DRY
The "Don't Repeat Yourself" (DRY) principle is about reducing repetitive statements in code. Following the DRY principle saves time and effort as there is less code, making the codebase easier to maintain and reducing the chance of bugs.

In our project, we implemented a utility file 'general.py', which consists of a collation of helper functions that can be called throughout the whole system. These helper functions divide our system functions into more manageable modules and also allows us to reuse code without repeating ourselves. 

An example of this is the helper function "valid_message" which checks if the provided message_id is valid (ie. exists in the database). This check is called in all the message functions and hence has been abstracted to reduce repetition in our code.

__Decorators__  
We have implemented decorators to make authentication more efficient, as most of our backend functions check if a provided token is valid before performing their tasks.
Originally, this was done by checking if our decode_token function returned -1 as a u_id however, by abstracting this functionality into a wrapper, we have applied the DRY principle. Overall, we were able to replace our previous, repetitive authentication checks with a simple decorator at the top of each function. 

Keeping our code DRY is essential in reducing viscosity, rigidity and needless repetition within our codebase. Creating modules makes code more unified and quicker to modify in the future as changes only need to be applied in one location. Modules also improve the mobility of code, also increasing reusability.

## KISS
The "Keep it Simple Stupid" (KISS) principle refers to keeping code clear and easy to understand. A solution to reducing the complexity of a piece of code is to break it down into smaller methods and also follow the "Single Responsibility Principle" (SPR). 

By dividing any large, multi-functional methods into multiple smaller blocks it,
	* makes the code more understandable
	* makes the code easier to modify
	* takes less time to update.

Our utility file 'general.py' allows us to abstract the complexities in our code and call helper functions which each execute one task. This behaviour is exemplified in our helper function "less_than_char" whose core functionality is to check if a string is less than a certain length. This removes some complexity from our functions "user_profile_sethandle" and "user_profile_setname", making it easier to understand and also makes our program more DRY.

Through keeping our codebase simple, stupid, we allow future developers to easily understand and modify our functions if necessary, by reducing opacity and needless complexity.

## Top Down Thinking
Top Down Thinking refers to the practice of working from high levels of thinking to lower levels of abstraction when creating functions. This approach can sometimes add overly complex abstractions and unnecessary separation, which often needs refactoring afterwards.

We've employed this practice since iteration 1 was released, in the form of stub functions for the backend. These stub functions took in parameters that we assumed would remain in a similar format when iteration 2 would be released (e.g. tokens, u_id etc). For example, once the core functionality of our stub functions was completed, we expanded overall functionality by writing the (previously assumed) helper functions in 'general.py'. 

By applying top down thinking design principles and fleshing out said functions when the specification became more detailed, it made the transition from iteration 1 to iteration 2 go smoothly, and without needing many major changes to our stub functions.

## Single Responsibility Principle
Single Responsibility Principle (SRP) ensures that each function is only responsible for one task.
We have done this by creating helper functions in our utility file 'general.py'. This allows each function in our API to have a single responsibility and improves readability and modularity. For example, when our database structure had to be altered (because of specification clarifications), we would've only needed to change the respective helper function. 
Additionally, code is much easier to understand since meaningfully named helper functions reduce complexity and increases readability. 

Two of our functions, message/sendlater and standup/send originally had the flask threading components in server.py and the actual functionality (checking, appending to the data structure) in their respective files in our component/ folder. We realised that we could reduce coupling between our backend function files and the flask server by moving the timers within the individual files as the two components are less interdependent, thus, adhering to the Single Responsibility Principle. 

Some functions in our flask routes, such as 'auth/passwordreset/request' would not satisfy SRP as it isn't possible to move the flask_mail functionality into a file/function separate to server.py. Therefore in *some cases*, we deemed it unnecessary to employ SRP.

Despite improving many aspects of our design, "general.py" is inherent to a degree of fragility, where if a change is made in a helper function which is used across many files, the code would be very easy to break. This is not a large concern as the file would be easy to fix, and overall complies with good design principles