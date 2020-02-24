// cowrie.c a simple shell


// PUT YOUR HEADER COMMENT HERE


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/wait.h>


// PUT EXTRA `#include'S HERE
#include <spawn.h>
#include <ctype.h> 
#include <stdbool.h>
#include <glob.h>

#define MAX_LINE_CHARS 1024
#define INTERACTIVE_PROMPT "cowrie> "
#define DEFAULT_PATH "/bin:/usr/bin"
#define WORD_SEPARATORS " \t\r\n"
#define DEFAULT_HISTORY_SHOWN 10

// These characters are always returned as single words
#define SPECIAL_CHARS "!><|"


// PUT EXTRA `#define'S HERE
#define NAME_MAX 255 

static void execute_command(char **words, char **path, char **environment);
static void do_exit(char **words);
static int is_executable(char *pathname);
static char **tokenize(char *s, char *separators, char *special_chars);
static void free_tokens(char **tokens);


// PUT EXTRA FUNCTION PROTOTYPES HERE
static bool is_number(char *string);
static int num_args(char **words);
static void change_directory(char **words);
static void print_directory(char **words);
static char *search_command(char **words, char **path);
static void spawn_process(char **words, char **path, char **environment);
static void output_command(int read, char **words);
static void store_in_history(char **words);
static int history_len(char *path);
static void print_history(char **words);
static void execute_history(char **words, char **path, char **environment);
static void update_arguments(char **words, glob_t matches, int arg);
static char **remove_output_direction(int mode, char **words);
static void free_new_args(char **words, int length);
static int output_mode(char **words);

int main(void) {
    //ensure stdout is line-buffered during autotesting
    setlinebuf(stdout);

    // Environment variables are pointed to by `environ', an array of
    // strings terminated by a NULL value -- something like:
    //     { "VAR1=value", "VAR2=value", NULL }
    extern char **environ;

    // grab the `PATH' environment variable;
    // if it isn't set, use the default path defined above
    char *pathp;
    if ((pathp = getenv("PATH")) == NULL) {
        pathp = DEFAULT_PATH;
    }
    char **path = tokenize(pathp, ":", "");

    char *prompt = NULL;
    // if stdout is a terminal, print a prompt before reading a line of input
    if (isatty(1)) {
        prompt = INTERACTIVE_PROMPT;
    }

    // main loop: print prompt, read line, execute command
    while (1) {
        if (prompt) {
            fputs(prompt, stdout);
        }

        char line[MAX_LINE_CHARS];
        if (fgets(line, MAX_LINE_CHARS, stdin) == NULL) {
            break;
        }

        char **command_words = tokenize(line, WORD_SEPARATORS, SPECIAL_CHARS);
        execute_command(command_words, path, environ);
        free_tokens(command_words);

    }

    free_tokens(path);
    return 0;
}


//
// Execute a command, and wait until it finishes.
//
//  * `words': a NULL-terminated array of words from the input command line
//  * `path': a NULL-terminated array of directories to search in;
//  * `environment': a NULL-terminated array of environment variables.
//
static void execute_command(char **words, char **path, char **environment) {
    assert(words != NULL);
    assert(path != NULL);
    assert(environment != NULL);

    char *program = words[0];

    if (program == NULL) {
        // nothing to do
        return;
    }

    if (strcmp(words[0], "!") == 0) {
        execute_history(words, path, environment);
        return; 
    }

    if (strcmp(program, "history") == 0) {
        print_history(words);
        store_in_history(words);
        return; 
    }

    // Stores the last command in the history file
    store_in_history(words);

    if (strcmp(program, "exit") == 0) {
        do_exit(words);
        // do_exit will only return if there is an error
        return;
    }

    // Change directory command 
    if (strcmp(program, "cd") == 0) {
        change_directory(words); 
        return;
    }

    if (strcmp(program, "pwd") == 0) {
        print_directory(words); 
        return;  
    }

    // CHANGE CODE BELOW HERE TO IMPLEMENT SUBSET 1
    // Path for command not given
    
    spawn_process(words, path, environment);
      
    return; 
}


// PUT EXTRA FUNCTIONS HERE

// Checks if a string is a number 
// RETURN VALUE: (true) if it is a number otherwise it returns (false)
static bool is_number(char *string) {
    for (char *c = &string[0]; *c != '\0'; c++) {
        if (!isdigit(*c)) {
            return false; 
        }
    }
    return true; 
}

// Implements the 'cd' command in cowrie using chdir 
static void change_directory(char **words) {
    char *dir = words[1]; 

    if (dir == NULL) {
        if (chdir(getenv("HOME")) != 0) {
            perror("cd"); 
        }
        return; 
    } else if (words[2] != NULL) {
        fprintf(stderr, "cd: too many arguments\n"); 
        return; 
    }

    if (chdir(dir) != 0) {
        fprintf(stderr, "cd: %s: No such file or directory\n", words[1]); 
        return;  
    } 

    return; 
}

// Implements the 'pwd' command in cowrie using getcwd
static void print_directory(char **words) {
    if (words[1] != NULL) {
        fprintf(stderr, "pwd: too many arguments\n");
        return; 
    }

    char *buffer = malloc(NAME_MAX); 
    if (getcwd(buffer, NAME_MAX) == NULL) {
        perror("pwd");
    }

    printf("current directory is '%s'\n", buffer); 
    free(buffer); 

    return; 
}

// Searches for command in $PATH 
// RETURN VALUE: (char *) if program exists and can be executed otherwise 
// returns NULL 
// NOTE: Caller has to manually free the return value 
static char *search_command(char **words, char **path) {
    char *program = words[0]; 

    // Iterates through the paths in the environment variable 
    char *str = malloc(BUFSIZ); 
    for (int i = 0; path[i] != NULL; i++) {
        snprintf(str, BUFSIZ, "%s/%s", path[i], program);
        if (is_executable(str)) { 
            return str; 
        }
    }
    
    return NULL; 
}

// Returns the total amount of arguments 
static int num_args(char **words) {
    int len = 0; 
    for (int i = 0; words[i] != NULL; i++) {
        len++;
    }
    return len; 
}

// Determines the output re-direction determined by words
// RETURN VALUE: (int) 0 is returned if no output re-direction is specified,
// (int) 1 is returned if overwrite output re-direction is specified, 
// (int) 2 is returned if append output re-direction is specified, 
// (int) -1 is returned if an error has occured 
static int output_mode(char **words) {
    int len = num_args(words); 

    if (strcmp(words[len - 1], ">") == 0) {
        fprintf(stderr, "invalid output redirection\n");
        return -1; 
    }

    for (int i = 0; words[i] != NULL; i++) {
        // '>' appears before the last 3 words of the command line 
        if (strcmp(words[i], ">") == 0 && i < len - 3) {
            fprintf(stderr, "invalid output redirection\n");
            return -1; 
        } else if (strcmp(words[i], ">") == 0 && i == len - 3) {
            if (strcmp(words[i + 1], ">") != 0) {
                fprintf(stderr, "invalid output redirection\n"); 
                return -1; 
            } else {
                return 2; 
            }
        } else if ((strcmp(words[i], ">") == 0) && i == len - 2) {
            return 1; 
        }
    }

    return 0; 
}

static int input_mode(char **words) {
    int len = num_args(words);    
    int mode = 0; 

    if (strcmp(words[0], "<") == 0) {
        mode = 1; 
    }

    for (int i = 1; i < len; i++) {
        if (strcmp(words[0], "<") == 0) {
            fprintf(stderr, "invalid input redirection\n"); 
            return -1; 
        }
    }

    return mode;
}

// Removes the '>' from the arguments 
// RETURN VALUE: (char **) which is the new set of arguments with output
// '>' removed 
// NOTE: Caller has to manually free the output using 'free_new_args'
static char **remove_output_direction(int mode, char **words) {
    int len = num_args(words); 
    char **new_args = malloc(len * sizeof(char *)); 
    if (mode == 1) {
        for (int i = 0; i < len - 2; i++) {
            new_args[i] = malloc(BUFSIZ); 
            strcpy(new_args[i], words[i]); 
        }
        new_args[len - 2] = NULL; 
    } else if (mode == 2) {
        for (int i = 0; i < len - 3; i++) {
            new_args[i] = malloc(BUFSIZ); 
            strcpy(new_args[i], words[i]); 
        }
        new_args[len - 3] = NULL; 
    } else {
        for (int i = 0; i < len; i++) {
            new_args[i] = malloc(BUFSIZ); 
            strcpy(new_args[i], words[i]); 
        }
        new_args[len] = NULL;
    }
    return new_args;  
}

// Frees the memory associated with the new arguments
// RETURN VALUE: (void)
static void free_new_args(char **words, int length) {
    for (int i = 0; i < length; i++) {
        free(words[i]); 
    }
    free(words); 
    return; 
}

// Creates a process using the given command and executes it 
// RETURN VALUE: (void)
static void spawn_process(char **words, char **path, char **environment) {
    char *program = words[0];

    // CODE BELOW FROM ANDREW TAYLOR 'spawn_read_pipe.c' 
    // pipe is created 
    int pipe_file_descriptors[2]; 
    if (pipe(pipe_file_descriptors) == -1) {
        perror("pipe"); 
        return; 
    }

    // create a list of file actions to be carried out on spawned process
    posix_spawn_file_actions_t actions;
    if (posix_spawn_file_actions_init(&actions) != 0) {
        perror("posix_spawn_file_actions_init");
        return;
    }

    // tell spawned process to close unused read end of pipe
    // without this - spawned process would not receive EOF
    // when read end of the pipe is closed below,
    if (posix_spawn_file_actions_addclose(&actions, pipe_file_descriptors[0]) != 0) {
        perror("posix_spawn_file_actions_init");
        return;
    }

    // tell spawned process to replace file descriptor 1 (stdout)
    // with write end of the pipe
    if (posix_spawn_file_actions_adddup2(&actions, pipe_file_descriptors[1], 1) != 0) {
        perror("posix_spawn_file_actions_adddup2");
        return;
    }

    // Invalid output redirection made 
    if (output_mode(words) == -1) {
        return; 
    }

    char *command;
    if (strrchr(program, '/') == NULL) {
        command = search_command(words, path); 
    } else {
        command = program; 
    }

    if (command == NULL) {
        fprintf(stderr, "%s: command not found\n", program);
        return; 
    }

    glob_t matches; 
    int totalMatches = 0; 
    char **new_words = remove_output_direction(output_mode(words), words); 

    for (int i = 1; words[i] != NULL; i++) {
        if (glob(words[i], GLOB_NOCHECK|GLOB_TILDE, NULL, &matches) == 0) {
            totalMatches++;
            update_arguments(words, matches, i); 
            continue;            
        }   
    }

    pid_t pid;
    if (posix_spawn(&pid, command, &actions, NULL, new_words, environment) != 0)
    {
        fprintf(stderr, "%s: command not found\n", command);
        return;
    }

    close(pipe_file_descriptors[1]); 

    output_command(pipe_file_descriptors[0], words); 

    int exit_status;
    if (waitpid(pid, &exit_status, 0) == -1) {
        perror("waitpid");
        return;
    }
    
    printf("%s exit status = %d\n", command, WEXITSTATUS(exit_status));
    free_new_args(new_words, num_args(new_words));

    return; 
}

// Prints the output to either stdout or to a specific file 
// RETURN VALUE: (void) 
static void output_command(int read, char **words) {
    // create a stdio stream from read end of pipe
    FILE *f = fdopen(read, "r");
    if (f == NULL) {
        perror("fdopen");
        return ;
    }

    // No ouput redirection specified 
    if (output_mode(words) == 0) {
        // read a line from read-end of pipe
        char output[BUFSIZ];
        while (fgets(output, BUFSIZ, f) != NULL) {
            printf("%s", output); 
        }
    } else if (output_mode(words) == 1) {
        FILE *output_file = fopen(words[num_args(words) - 1], "w"); 
        char output[BUFSIZ];
        while (fgets(output, BUFSIZ, f) != NULL) {
            fprintf(output_file, "%s", output); 
        }
        fclose(output_file); 
    } else if (output_mode(words) == 2) {
        FILE *output_file = fopen(words[num_args(words) - 1], "a");
        char output[BUFSIZ];
        while (fgets(output, BUFSIZ, f) != NULL) {
            fprintf(output_file, "%s", output); 
        }
        fclose(output_file);
    }

    fclose(f); 
    return; 
}

// Updates the arguments of words with the globbed files 
// RETURN VALUE: None
static void update_arguments(char **words, glob_t matches, int arg) {
    // Reallocates and clears memory 
    words[arg] = realloc(words[arg], strlen(matches.gl_pathv[0]) + 2);
    words[arg] = memset(words[arg], 0, strlen(matches.gl_pathv[0]) + 2);
    // Concactenates the string 
    for (int j = 0; j < matches.gl_pathc; j++) {
        // Reallocates length of string 
        words[arg] = realloc(words[arg], strlen(words[arg]) + strlen(matches.gl_pathv[j]) + 2);
        strcat(words[arg], matches.gl_pathv[j]);
        if (j != matches.gl_pathc - 1) {
            strcat(words[arg], " ");
        } 
    }
    return; 
}

// Stores the command in a file located in $HOME/.cowrie_history 
// RETURN VALUE: (void) on successful write 
static void store_in_history(char **words) {
    char *history_path = malloc(BUFSIZ); 

    // Path of history file for cowrie 
    snprintf(history_path, BUFSIZ, "%s/.cowrie_history", getenv("HOME")); 
    FILE *history = fopen(history_path, "a"); 

    if (history == NULL) {
        return; 
    }

    for (int i = 0; words[i] != NULL; i++) {
        fputs(words[i], history); 
        // No space appended if it is the last argument 
        if (words[i + 1] != NULL) {
            fputc(' ', history); 
        }
    }

    // Appends new line to the end of the command 
    fputc('\n', history); 

    // Cleans up after program
    free(history_path);
    fclose(history); 

    return; 
}

// Calcualtes the length of history 
// RETURN VALUE: (int) which is the length of history or -1 on error 
static int history_len(char *path) {
    FILE *history = fopen(path, "r");

    char *history_text = malloc(BUFSIZ); 
    int line_no = 0; 
    // Goes through history file line by line and adds to line_no 
    while (fgets(history_text, BUFSIZ, history)) {
        line_no++; 
    }

    // Cleans up the after the function 
    fclose(history); 
    if (history_text) {
        free(history_text);
    }

    return line_no; 
}

// Prints the history file in the format "%d: %s\n"
// RETURN VALUE: If history file does not exist, function will return and 
// silently fail
static void print_history(char **words) {
    char *history_path = malloc(BUFSIZ);

    // Path of history file for cowrie
    snprintf(history_path, BUFSIZ, "%s/.cowrie_history", getenv("HOME"));
    FILE *history = fopen(history_path, "r");

    struct stat s; 

    // History file does not exist 
    if (stat(history_path, &s) != 0) {
        free(history_path);
        fclose(history);
        return; 
    }

    int history_length = history_len(history_path);
    // Line_no to start printing history 
    int start = 0;  

    if (words[2] != NULL) {
        fprintf(stderr, "history: too many arguments\n");
        return;
    } else if (words[1] == NULL) {
        start = history_length - 10;
    } else {
        if (!is_number(words[1])) {
            fprintf(stderr, "history: %s: numeric argument required\n", words[1]);
            return; 
        }
        start = history_length - atoi(words[1]); 
    }

    char *history_text = malloc(BUFSIZ); 
    int line_no = 0; 
    while (fgets(history_text, BUFSIZ, history) != NULL) {
        if (line_no >= start) {
            printf("%d: %s", line_no, history_text);
        }  
        line_no++; 
    }

    // Cleans up after program runs 
    if (history_text) {
        free(history_text); 
    }
    free(history_path);
    fclose(history); 

    return; 
}

// Executes a command in history
static void execute_history(char **words, char **path, char **environment) {
    char *history_path = malloc(BUFSIZ);

    // Path of history file for cowrie
    snprintf(history_path, BUFSIZ, "%s/.cowrie_history", getenv("HOME"));
    FILE *history = fopen(history_path, "r");

    struct stat s; 

    // History file does not exist 
    if (stat(history_path, &s) != 0) {
        free(history_path);
        fclose(history);
        return; 
    }

    int execute_line; 
    if (words[1] == NULL) {
        execute_line = history_len(history_path) - 1; 
    } else {
        if (words[2] != NULL) {
            fprintf(stderr, "!: too many arguments\n");
            return; 
        }
        execute_line = atoi(words[1]);
    }

    char *history_text = malloc(BUFSIZ); 
    int line_no = 0; 
    while (fgets(history_text, BUFSIZ, history) != NULL) {
        if (line_no == execute_line) {
            printf("%s", history_text); 
            execute_command(tokenize(history_text, WORD_SEPARATORS, SPECIAL_CHARS), path, environment);
            // Cleans up after program runs 
            if (history_text) {
                free(history_text); 
            }
            return; 
        }
        line_no++; 
    }

    // Cleans up after program runs 
    if (history_text) {
        free(history_text); 
    }

    return; 
}
 
//
// Implement the `exit' shell built-in, which exits the shell.
//
// Synopsis: exit [exit-status]
// Examples:
//     % exit
//     % exit 1
//
static void do_exit(char **words) {
    int exit_status = 0;

    if (words[1] != NULL) {
        if (words[2] != NULL) {
            fprintf(stderr, "exit: too many arguments\n");
        } else {
            char *endptr;
            exit_status = (int)strtol(words[1], &endptr, 10);
            if (*endptr != '\0') {
                fprintf(stderr, "exit: %s: numeric argument required\n",
                        words[1]);
            }
        }
    }

    exit(exit_status);
}


//
// Check whether this process can execute a file.
// Use this function when searching through the directories
// in the path for an executable file
//
static int is_executable(char *pathname) {
    struct stat s;
    return
        // does the file exist?
        stat(pathname, &s) == 0 &&
        // is the file a regular file?
        S_ISREG(s.st_mode) &&
        // can we execute it?
        faccessat(AT_FDCWD, pathname, X_OK, AT_EACCESS) == 0;
}


//
// Split a string 's' into pieces by any one of a set of separators.
//
// Returns an array of strings, with the last element being `NULL';
// The array itself, and the strings, are allocated with `malloc(3)';
// the provided `free_token' function can deallocate this.
//
static char **tokenize(char *s, char *separators, char *special_chars) {
    size_t n_tokens = 0;
    // malloc array guaranteed to be big enough
    char **tokens = malloc((strlen(s) + 1) * sizeof *tokens);


    while (*s != '\0') {
        // We are pointing at zero or more of any of the separators.
        // Skip leading instances of the separators.
        s += strspn(s, separators);

        // Now, `s' points at one or more characters we want to keep.
        // The number of non-separator characters is the token length.
        //
        // Trailing separators after the last token mean that, at this
        // point, we are looking at the end of the string, so:
        if (*s == '\0') {
            break;
        }

        size_t token_length = strcspn(s, separators);
        size_t token_length_without_special_chars = strcspn(s, special_chars);
        if (token_length_without_special_chars == 0) {
            token_length_without_special_chars = 1;
        }
        if (token_length_without_special_chars < token_length) {
            token_length = token_length_without_special_chars;
        }
        char *token = strndup(s, token_length);
        assert(token != NULL);
        s += token_length;

        // Add this token.
        tokens[n_tokens] = token;
        n_tokens++;
    }

    tokens[n_tokens] = NULL;
    // shrink array to correct size
    tokens = realloc(tokens, (n_tokens + 1) * sizeof *tokens);

    return tokens;
}


//
// Free an array of strings as returned by `tokenize'.
//
static void free_tokens(char **tokens) {
    for (int i = 0; tokens[i] != NULL; i++) {
        free(tokens[i]);
    }
    free(tokens);
}
