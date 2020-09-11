# JScanner
Given a list of URL containing JS File, it scans for vulnerabilites. Useful for scripting with other command while still saving to a file.

# Usage
```
usage: JScanner [-h] [-w WORDLIST] [-oD OUTPUT_DIRECTORY] [-d DOMAIN] [-t THREADS] [-b]

Javascript Scanner

optional arguments:
  -h, --help            show this help message and exit
  -w WORDLIST, --wordlist WORDLIST
                        Absolute path of wordlist
  -oD OUTPUT_DIRECTORY, --output-directory OUTPUT_DIRECTORY
                        Output directory
  -d DOMAIN, --domain DOMAIN
                        Domain name
  -t THREADS, --threads THREADS
                        Number of threads
  -b, --banner          Print banner and exit

Enjoy bug hunting
```

# Example
Scan a single URLs  
* JScanner -w <(echo 'google.com') -oD `pwd` -t 1 -d google.com
Scan from URLs  
* JScanner -w /tmp/files.txt -oD `pwd` -t 10 -d anydomainnameinfiles.txt.com
