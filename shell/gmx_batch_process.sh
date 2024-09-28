#!/bin/bash

# 生成小分子所需的gro，top，以及itp文件
sobtop() {
  mol_file=$1
  file_name=$(basename "$mol_file")
  file_dir=$(dirname "$mol_file")
  name="${file_name%.*}"
  
  path="$file_dir/../kotori_results/$name/"
  echo $path
  # echo $file_name
  if [ ! -d $path ];then
    mkdir -p $path
  fi
  
  gro_path="$path/$name.gro"
  top_path="$path/$name.top"
  itp_path="$path/$name.itp"
  printf "$1\n2\n$gro_path\n1\n2\n4\n$top_path\n$itp_path\n0\n" | ./sobtop
  echo '#ifdef POSERS' >> $itp_path
  echo '#include "posre.itp"' >> $itp_path # attention
  echo '#endif' >> $itp_path

  tgt_file="$file_dir/../protein/topol.top" 
  line=`grep -n '#include "topol_Protein_chain_A.itp"' $tgt_file | cut -d ":" -f1`
  sed '/; Include chain topologies/{n; s|^#include "|#include "../../protein/|; :a; n; /^; Include /!{ s|^#include "|#include "../../protein/|; ba; }}' $tgt_file > "$path/topol.top"  
  sed -i "24i #include \"$name.itp\"" "$path/topol.top"
  echo "$name     1" >> "$path/topol.top"
}


combine() {
  mol_file=$1
  mol_file_name=$(basename "$mol_file")
  mol_file_dir=$(dirname "$mol_file")
  mol_name="${mol_file_name%.*}"
    

  mol_gro_path="$mol_file_dir/../kotori_results/$name/$name.gro"
  protein_gro_path=$2

  n_mol_line=`wc -l $mol_gro_path`
  n_mol_atom=`sed -n "2 p" $mol_gro_path`
  
  n_protein_atom=`sed -n "2 p" $protein_gro_path`

  total_atom=$((n_protein_atom + n_mol_atom))
  
  out_file="$mol_file_dir/../kotori_results/$name/$mol_name-complex.gro"
  head -n 1 $protein_gro_path > $out_file
  echo $total_atom >> $out_file
  head -n -1 $protein_gro_path | tail -n +3 >> $out_file
  head -n -1 $mol_gro_path | tail -n +3 >> $out_file
  tail -n 1 $protein_gro_path >> $out_file
}


gen_posre() {
  mol_file=$1
  mol_file_name=$(basename "$mol_file")
  mol_file_dir=$(dirname "$mol_file")
  mol_name="${mol_file_name%.*}"

  mol_gro_path="$mol_file_dir/../kotori_results/$name/$name.gro"
  
  out_file="$mol_file_dir/../kotori_results/$name/posre.itp"
  printf "0\n" | gmx genrestr -f $mol_gro_path -o $out_file
}


main() {
  mol_file=$1
  mol_file_name=$(basename "$mol_file")
  mol_file_dir=$(dirname "$mol_file")
  mol_name="${mol_file_name%.*}"

  root="$mol_file_dir/../kotori_results/$name"
  work="$mol_file_dir/.."  

  box_in="$root/$mol_name-complex.gro"
  box_out="$root/protein_box.gro"

  water_out="$root/protein_sol.gro"
  topol_file="$root/topol.top"
  
  tpr_out="$root/em.tpr"
  iron_out="$root/system.gro"
  
  fin_in="$root/md.tpr"

  gpu=$2
  gmx editconf -f $box_in -o $box_out -d 1.0 -bt cubic && \
    gmx solvate -cp $box_out -o $water_out -p $topol_file && \
    gmx grompp -f "$work/em.mdp" -c $water_out -r $water_out -p $topol_file -o $tpr_out -maxwarn 1 && \
    printf "15\n" | gmx genion -s $tpr_out -p $topol_file -o $iron_out -neutral -conc 0.15 && \
    gmx grompp -f "$work/em.mdp" -c $iron_out -r $iron_out -p $topol_file -o $tpr_out && \
    pushd $root && gmx mdrun -v -deffnm em -ntmpi 1 -ntomp 16 -gpu_id $gpu && popd && \
    gmx grompp -f "$work/md.mdp" -c "$root/em.gro" -r "$root/em.gro" -p $topol_file -o $fin_in && \
    pushd $root && gmx mdrun -v -deffnm md -ntmpi 1 -ntomp 16 -gpu_id $gpu && popd && echo 'done'
}


WORK_PATH=$1
MOL_DIR=$2
GPU=$3

find "$WORK_PATH/$MOL_DIR" -type f | while read -r file; do
    sobtop "$file" && combine $file "$WORK_PATH/protein/protein.gro" && gen_posre $file && main $file $GPU
done

# combine $1 $2
