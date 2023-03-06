/* ------------------------------------------------------------------
 * nextline.c -- get the next line of a text file.
 * 								
 * Author:							
 * Craig H. Rowland <crowland@psionic.com> 15-JAN-96		
 *		    <crowland@vni.net>				
 *  for the original logtail.c
 * Moses Moore <moc.iazom@sesom>
 *  for hacking it into nextline.c
 *								
 * This program will read in a standard text file starting from an
 * offset marker (or start of file if there is none) and return the
 * next sequence of characters up to and including the next newline,
 * or EOF.  It will write the location of that newline to an offset
 * marker, so it will start from there on subsequent launches.
 *								
 * This program covered by the GNU License.
 * This program is free to use as long as the above copyright
 * notices are left intact.  This program has no warranty of any kind.	
 * Share and enjoy!
 *								
 * VERSION 1.1: Initial release	 of logtail.c				
 *         1.11: Minor typo fix. Fixed NULL comparison.
 *         1.11a: hacked to read only one line at a time.
 * ------------------------------------------------------------------
 */


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sysexits.h>
#include <unistd.h>
#include <sys/stat.h>
#include <sys/types.h>


#define MAX_LINE 65536 /* buffer; max length for a line of text */
#define MAX_PATH 255 /* increase this size if you need a longer path */
#define VERSION "1.11a"


/* Prototypes */
void usage(void);
int get_line(char *txtfilename, char *offset_filename);

int main(int argc, char *argv[]) {

  int status=1; /* Set status flag to error */
  char offset_filename[MAX_LINE];

  /* Check args */
  if((argc < 2) || (argc > 3)) {
    usage();
    exit(EX_USAGE);
    }

  /* Do sanity check on all user supplied data */
  if ((strlen(argv[1])) > MAX_PATH - 8) {
    /* longer than MAX_PATH characters? */
    printf("Input filename %s is too long.\n",argv[1]);
    exit(EX_DATAERR);
  }

  if (argc == 3) {
    /* check user supplied alternate filename */
    if ((strlen(argv[2])) > MAX_PATH - 8 ) {
      /* longer than MAX_PATH characters? */
      printf("Input filename %s is too long.\n",argv[1]);
      exit(EX_DATAERR);
    }
    strcpy(offset_filename,argv[2]);
  }
  else {
    /* If no alternate filename given, make our own */
    strcpy(offset_filename,argv[1]);
    strcat(offset_filename,".offset");
  }

  status=get_line(argv[1], offset_filename); /* check the logs */

  if(status == 0)
    exit(EX_OK);
  else if(status == 1)
    exit(EX_SOFTWARE);
  else if(status == 2)
    exit(EX_NOINPUT);
  else if(status == 3)
    exit(EX_DATAERR);
  else if(status == 4)
    exit(EX_CANTCREAT);
  else {
    printf("An unknown error has occurred\n\n");
    exit(EX_SOFTWARE);
  }

}


int get_line(char *txtfilename, char *offset_filename) {

  FILE *input,		/* Value user supplies for input file */
       *offset_output;	/* name of the offset output file */

  struct stat file_stat;

  char inode_buffer[MAX_LINE],		/* Inode temp storage */
       offset_buffer[MAX_LINE], 	/* Offset temp storage */
       buffer[MAX_LINE];		/* I/O Buffer */

  long offset_position;	/* position in the file to offset */

  /* Check if the file exists in specified directory */
  /* Open as a binary in case the user reads in non-text files */
  if((input=fopen(txtfilename, "rb")) == NULL) {
    printf("File %s cannot be read.\n",txtfilename);
    return(2);
  }

  /* see if we can open an existing offset file and read in the inode */
  /* and offset */
  if((offset_output=fopen(offset_filename, "rb")) != NULL) {
    /* read in the saved inode number */
    if((fgets(buffer,MAX_LINE,offset_output)) !=NULL) {
      /* nested if()...yuch */
      strcpy(inode_buffer,buffer); /* copy in inode */
    }
    /* read in the saved decimal offset */
    if((fgets(buffer,MAX_LINE,offset_output)) !=NULL) {
      /* nested if()...yuch */
      strcpy(offset_buffer,buffer); /* copy in offset */
    }
    fclose(offset_output); /* We're done, clean up */
  }
  else {
    /* can't read the file? then assume no offset file exists */
    strcpy(inode_buffer,"0"); /* this inode will be set later */
    offset_position=0L; /* if the file doesn't exist, assume */
      	    /* offset of 0 because we've never */
      	    /* tailed it before */
  }


  if((stat(txtfilename,&file_stat)) != 0) /* load struct */ {
    printf("Cannot get %s file size.\n",txtfilename);
    return(3);
  }					

  /* if the current file inode is the same, but the file size has */
  /* grown SMALLER than the last time we checked, then something  */
  /* suspicous has happened (log file edited) and we'll report it */
  if(((atol(inode_buffer)) == (file_stat.st_ino))
     && (atol(offset_buffer) > (file_stat.st_size))) {
 	 	offset_position=0L; /* reset offset and report everything */
    printf("(Text file %s is smaller than offset; starting from the top again)\n",txtfilename);
  }

  /* if the current file inode or size is different than that in the */
  /* offset file then assume it has been rotated and set offset to zero */
  if(((atol(inode_buffer)) != (file_stat.st_ino))
     || (atol(offset_buffer) > (file_stat.st_size))) {
    offset_position=0L;
  }
  else {
    /* If the file inode is the same as old inode set the new offset */
    offset_position=atol(offset_buffer); /*get value and convert */
  }

#ifdef DEBUG
printf("inodebuf: %s offsetbuf: %s offsetpos: %ld\n",inode_buffer,offset_buffer,offset_position);
#endif

  fseek(input, offset_position, 0); /* set the input file stream to */
      		  /* the offset position */
  /* Get one line.  Print it. */
  if ( fgets(buffer,MAX_LINE,input) !=NULL) {
    printf("%s",buffer);
  }

  /* after we are done we need to write the new offset */
  if((offset_output=fopen(offset_filename, "w")) == NULL) {
    printf("File %s cannot be created. Check your permissions.\n",offset_filename);
    fclose(input);
    fclose(offset_output);
    return(4);
  }
  else {
    if ((chmod(offset_filename,00600)) != 0) {
      /* Don't let anyone else read offset */
      printf("Cannot set permissions on file %s\n",offset_filename);
      return(3);
    }
    else {
      offset_position=ftell(input); /* set new offset */
      fprintf(offset_output,"%ld\n%ld",(long)file_stat.st_ino,offset_position);
      /* write it */
    }
  }
  fclose(input); /* clean up */
  fclose(offset_output);

  return(0); /* everything A-OK */
}


/* Tell them how to use this */
void usage(void) {
  printf("nextline: version %s \n\n",VERSION);
  printf(" by Craig H. Rowland <crowland@psionic.com> and Moses <moc.iazom@sesom>\n");
  printf("Based upon original utility: retail (c)Trusted Information Systems\n");
  printf("This program is covered by the GNU license.\n\n");
  printf("Usage: nextline [TXT_FILE] <offset_file>\n");
  printf("  Print the next line of text.\n\n");
  printf("  Remembers where it left off by writing to a file called\n");
  printf("  [TXT_FILE].offset in the same directory that will contain the\n");
  printf("  decimal offset and inode of the file in ASCII format. \n");
  printf("  The optional <offset_file> parameter can be used to specify your\n");
  printf("  own name for the offset file. \n\n");
}

