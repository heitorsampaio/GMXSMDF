#!/usr/local/bin/perl

use Term::ANSIColor qw(:constants);

print BLUE, "
██████╗  █████╗ ████████╗ ██████╗ ███████╗███╗   ██╗
██╔══██╗██╔══██╗╚══██╔══╝██╔════╝ ██╔════╝████╗  ██║
██████╔╝███████║   ██║   ██║  ███╗█████╗  ██╔██╗ ██║
██╔═══╝ ██╔══██║   ██║   ██║   ██║██╔══╝  ██║╚██╗██║
██║     ██║  ██║   ██║   ╚██████╔╝███████╗██║ ╚████║
╚═╝     ╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚══════╝╚═╝  ╚═══╝
       Patologia Molecular e Medicina Genômica
                                                coded by Heitor Sampaio;\n", RESET;



print "+++ This script is toolbox for Gromacs Molecular Dynamics simulation, you can run all gromacs simulations\n";

$user = &promptUser("Enter your name ");

print "\n[+] Please enter with the specifications of your simulation below, $user ...\n\n";


sub prompt {
  my ($query) = @_; # take a prompt string as argument
  local $| = 1; # activate autoflush to immediately show the prompt
  print $query;
  chomp(my $answer = <STDIN>);
  return $answer;
}

sub prompt_yn {
  my ($query) = @_;
  my $answer = prompt("$query (Y/N): ");
  return lc($answer) eq 'y';
}

if (prompt_yn("Do you want to run a complex simulation? ")){
  print("Would you like to run GPU(1) script or noGPU(0)? ");
    my $gpuNOgpu = <STDIN>;
    $strucDir = &promptUser("Enter the structure file directory ", "/home/user/USERNAME/...");
    $folderName = &promptUser("Enter the desired folder name ");
    $ligName = &promptUser("Enter the Ligand .gro file ");
    $tcgrps = &promptUser("Enter the tc groups ", "Ex. Protein_LIGNAME");
    if ($gpuNOgpu == 0) {
      system('python3', 'complex/complex_nogpu.py', '-s', $strucDir, '-f', $folderName, '-mdt', $mdTime, '-l', $ligName, '-tcgrps', $tcgrps) == 0 or die "Python script returned error $?";
    } else {
      if ($gpuNOgpu == 1){
        system('python3', 'complex/complex_gpu.py', '-s', $strucDir, '-f', $folderName, '-mdt', $mdTime, '-l', $ligName, '-tcgrps', $tcgrps) == 0 or die "Python script returned error $?";
      }
    }
  }


if (prompt_yn("Do you want to continue a checkpointed simulation? ")){
  print("Would you like to run GPU(1) script or noGPU(0)? ");
    my $gpuNOgpu = <STDIN>;
      $cptDir = &promptUser("Enter the folder directory ", "/home/user/USERNAME/...");
    if ($gpuNOgpu == 0) {
      system('python3', 'gmxsmdf_checkpoint_nogpu.py', '-s', $strucDir, '-f', $folderName) == 0 or die "Python script returned error $?";
    } else {
      if ($gpuNOgpu == 1){
        system('python3', 'gmxsmdf_checkpoint_gpu.py', '-s', $strucDir, '-f', $folderName) == 0 or die "Python script returned error $?";
      }
    }
  }

  if (prompt_yn("Do you want to run a simple Molecular Dynamicss simulation? ")){
  }

$strucDir = &promptUser("Enter the structure file directory ", "/home/user/USERNAME/...");
$folderName = &promptUser("Enter the desired folder name ");


print("Enter the MD simulation time in NS: ");
my $nsTIME = <STDIN>;
my $NS = 0.001;
my $nSTE = 1000;
my $gM = 2;

$nsPS = $nsTIME / $NS;
$nsToNSTE = $nsPS * $nSTE;
$mdTime = $nsToNSTE / $gM;

print("Would you like to run GPU(1) script or noGPU(0)? ");
my $gpuNOgpu = <STDIN>;


print "$gpuNOgpu, $strucDir, $folderName, $mdTime\n";

sub promptUser {

   local($promptString,$defaultValue) = @_;

   if ($defaultValue) {
      print $promptString, "[", $defaultValue, "]: ";
   } else {
      print $promptString, ": ";
   }

   $| = 1;               # force a flush after our print
   $_ = <STDIN>;         # get the input from STDIN (presumably the keyboard)
   #$gpuNogpu = "noGPU";

   chomp;

   if ("$defaultValue") {
      return $_ ? $_ : $defaultValue;    # return $_ if it has a value
   } else {
      return $_;
   }

}

  if ($gpuNOgpu == 0) {
    print "\n[+] The simulation is now running without GPU support, good luck, you will need xD, $user ...\n\n";
    system('python3', 'gmxsmdf_nogpu.py', '-s', $strucDir, '-f', $folderName, '-mdt', $mdTime) == 0 or die "Python script returned error $?";
  } else {
    if ($gpuNOgpu == 1){
      print "\n[+] The simulation is now running with GPU support, good luck, you will need xD, $user ...\n\n";
      system('python3', 'gmxsmdf_gpu.py', '-s', $strucDir, '-f', $folderName, '-mdt', $mdTime) == 0 or die "Python script returned error $?";
    }
  }


print "\n[+] Thanx for running my script ˆˆ, $user ...\n\n";
