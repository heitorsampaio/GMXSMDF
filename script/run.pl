#!/usr/local/bin/perl


use Term::ANSIColor qw(:constants);

print GREEN, "
██████╗  █████╗ ████████╗ ██████╗ ███████╗███╗   ██╗
██╔══██╗██╔══██╗╚══██╔══╝██╔════╝ ██╔════╝████╗  ██║
██████╔╝███████║   ██║   ██║  ███╗█████╗  ██╔██╗ ██║
██╔═══╝ ██╔══██║   ██║   ██║   ██║██╔══╝  ██║╚██╗██║
██║     ██║  ██║   ██║   ╚██████╔╝███████╗██║ ╚████║
╚═╝     ╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚══════╝╚═╝  ╚═══╝
       Patologia Molecular e Medicina Genômica
                                                coded by Heitor Sampaio;\n", RESET;



print "+++ This script is for runing a simple Molecular Dynamics simulation\n";

$user = &promptUser("Enter your name ");

print "\n[+] Please enter with the specifications of your simulation below, $user ...\n\n";

$strucDir = &promptUser("Enter the structure file directory ", "/home/user/USERNAME/...");
$folderName = &promptUser("Enter the desired folder name ");
$mdTime = &promptUser("Enter the MD simulation time ", "2 * 500000 = 1000 ps (1 ns)");

print "$strucDir, $folderName, $mdTime\n";

sub promptUser {

   local($promptString,$defaultValue) = @_;

   if ($defaultValue) {
      print $promptString, "[", $defaultValue, "]: ";
   } else {
      print $promptString, ": ";
   }

   $| = 1;               # force a flush after our print
   $_ = <STDIN>;         # get the input from STDIN (presumably the keyboard)


   chomp;

   if ("$defaultValue") {
      return $_ ? $_ : $defaultValue;    # return $_ if it has a value
   } else {
      return $_;
   }
}

print "\n[+] The simulation is now running, good luck, you will need xD, $user ...\n\n";

system('python3', 'gmxsmdf_gpu.py', '-s', $strucDir, '-f', $folderName, '-mdt', $mdTime) == 0 or die "Python script returned error $?";

print "\n[+] Thanx for running my script ˆˆ, $user ...\n\n";
