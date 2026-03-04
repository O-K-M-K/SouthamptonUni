Require Import Arith List.
Require Import Arith.        (* general nat arithmetic lemmas *)
Require Import Lia.          (* the `lia` tactic for linear arithmetic *)
(* Require Import Arith.Mult.   multiplication specific lemmas *)
Require Import PeanoNat.     (* Nat.* lemmas, e.g. Nat.mul_comm *)

Definition Memory : Type := list nat.
Definition Stack : Type := list nat.
Definition Address : Type := nat.

Fixpoint read (addr : Address) (default : nat) (mem : Memory) : nat :=
match addr, mem with
| _, nil => default (*memory is empty list => return empty list*)
| 0, x :: _ => x (*read from addr 0 take head of list and return it*)
| S n, _ :: xs => read n default xs (*read from addr Sn take head off and reduce n by one then recurse*)
end.

Fixpoint write (addr : Address) (value : nat) (mem : Memory) : Memory :=
match addr, mem with
| _, nil => nil (*memory is emptly list => return empty list*)
| 0, _ :: xs => value :: xs (*address is zero write to front of xs *)
| S n, x :: xs => x :: write n value xs (*move through list till addr value reached then write there*)
end.

Inductive Instruction : Type :=
| load  : Address -> Instruction
| const : nat ->     Instruction
| add   :            Instruction
| sub   :            Instruction
| mul   :            Instruction
| store : Address -> Instruction
| goto  : Address -> Instruction
| ifeq  : Address -> Instruction
| halt  :            Instruction.

Definition Program : Type := Address -> Instruction.

Record Machine : Type := {
  pc : Address;
  program : Program;
  locals : Memory;
  stack : Stack;
}.

Definition fetch (m : Machine) : Instruction := program m (pc m).

Definition execute_single_instruction (m : Machine) : Machine :=
match fetch m, stack m with
| load addr, s => {|
  pc := pc m + 1;
  program := program m;
  locals := locals m;
  stack := read addr 0 (locals m) :: s;
|}
| const c, s => {|
  pc := pc m + 1;
  program := program m;
  locals := locals m;
  stack := c :: s;
|}
| add, x :: y :: s => {|
  pc := pc m + 1;
  program := program m;
  locals := locals m;
  stack := x + y :: s;
|}
| sub, x :: y :: s => {|
  pc := pc m + 1;
  program := program m;
  locals := locals m;
  stack := y - x :: s;
|}
| mul, x :: y :: s => {|
  pc := pc m + 1;
  program := program m;
  locals := locals m;
  stack := y * x :: s;
|}
| goto addr, s => {|
  pc := addr;
  program := program m;
  locals := locals m;
  stack := s;
|}
| ifeq addr, 0 :: s => {|
  pc := addr;
  program := program m;
  locals := locals m;
  stack := s;
|}
| ifeq addr, _ :: s => {|
  pc := pc m + 1;
  program := program m;
  locals := locals m;
  stack := s;
|} 
| store addr, x :: s => {|
  pc := pc m + 1;
  program := program m;
  locals := write addr x (locals m);
  stack := s;
|}
| _, _ => m
end.

Fixpoint execute_n_instructions (n : nat) (m : Machine) : Machine :=
match n with
| 0 => m
| S n => execute_n_instructions n (execute_single_instruction m)
end.

Lemma execute_n_single_comm (a: nat) : forall m,
execute_n_instructions a (execute_single_instruction m) = execute_single_instruction (execute_n_instructions a m).
Proof. induction a as [ | a' IHa'].
  - simpl. reflexivity.
  - intros m. simpl. rewrite -> IHa'. reflexivity.
Qed.

Lemma execute_instruction_succ' (a : nat) : forall m,
execute_single_instruction (execute_n_instructions a m) = execute_n_instructions (S a) m.
Proof. induction a as [ | a' IHa']. 
  - simpl. reflexivity.
  - simpl. intros m. rewrite <- execute_n_single_comm. reflexivity.
Qed.


Lemma execute_instruction_succ (a : nat) : forall m,
execute_single_instruction (execute_n_instructions a m) = execute_n_instructions (S a) m.
Proof. induction a as [ | a' IHa']. 
  - simpl. reflexivity.
  - intros m. simpl. rewrite -> IHa'. simpl. reflexivity.
Qed.

Lemma execute_plus_instructions (a : nat) : forall b m,
execute_n_instructions (a + b) m = execute_n_instructions a (execute_n_instructions b m).
Proof. induction a as [ | a' IHa'].
  - simpl. reflexivity.
  - simpl. intros b m. rewrite -> IHa'. rewrite execute_n_single_comm. reflexivity.
Qed.



(* Part 1, 6 marks *)

Definition expt (n m : nat) : nat := n ^ m.

Fixpoint expt_iter (n m acc : nat) :=
match m with
| 0 => acc
| S m' => expt_iter n m' (n * acc)
end.

(* Always induct on m when dealing with expt_iter *)
Lemma expt_iter_equivalent_acc (n m : nat) : 
forall acc, expt_iter n m acc = acc * expt n m.
Proof. induction m as [| m' IHm'];  intros acc. 
    - simpl. ring.
    - simpl. rewrite IHm'. ring.
Qed.

Theorem expt_iter_equivalent (n m : nat) : 
expt_iter n m 1 = expt n m.
Proof. induction m as [| m' IHm'].
    - reflexivity.
    - simpl. rewrite expt_iter_equivalent_acc. ring.
Qed. 

(*  Part 2, 12 marks *)

Definition expt_program : Program := fun pc =>
match pc with
| 0 =>  const 1
| 1 =>  store 2
| 2 =>  load 1
| 3 =>  ifeq 14
| 4 =>  load 1
| 5 =>  const 1
| 6 =>  sub
| 7 =>  store 1
| 8 =>  load 0
| 9 =>  load 2
| 10 => mul
| 11 => store 2
| 12 => goto 2
| 13 => load 2
| _ => halt
end.

Definition read_acc (m : Machine) : nat := read 2 0 (locals m).

Fixpoint expt_loop_instructions (m : nat) : nat :=
match m with
| 0 => 2
| S m => 11 + expt_loop_instructions m
end.

Definition expt_total_instructions (m : nat) : nat :=
2 + expt_loop_instructions m.

Definition jvm_expt (n m : nat) : Machine :=
execute_n_instructions (expt_total_instructions m) {|
  pc := 0;
  program := expt_program;
  locals := n :: m :: 0 :: nil;
  stack := nil
|}.


Lemma expt_loop_succ (n : nat):
    expt_loop_instructions (S n) = 11 + expt_loop_instructions n.
Proof. reflexivity. Qed.

(* running program for 1 defined loop results in expected result *)
Lemma expt_loop_body (n m acc : nat) :
  execute_n_instructions 11 {|
    pc := 2;
    program := expt_program;
    locals := n :: S m :: acc :: nil;
    stack := nil
  |} = {|
    pc := 2;
    program := expt_program;
    locals := n :: S m - 1 :: n * acc :: nil;
    stack := nil
  |}.
Proof. reflexivity. Qed.


(* evaluating two loops one loop behind results in evaluting one loop *)
Lemma evaluate_one_loop (n m acc: nat): 
execute_n_instructions (expt_loop_instructions (S m)) {|
    pc := 2;
    program := expt_program;
    locals := n :: S m :: acc :: nil;
    stack := nil
|} = execute_n_instructions (expt_loop_instructions (m)) {|
    pc := 2;
    program := expt_program;
    locals := n :: S m - 1 :: n * acc :: nil;
    stack := nil
|}. 
Proof. 
    rewrite expt_loop_succ.
    rewrite Nat.add_comm.
    rewrite execute_plus_instructions.
    rewrite expt_loop_body.
    reflexivity.
Qed.

(* jvms acc upon halt results in same value as expt_iter n m acc *)
Lemma jvm_expt_iter (n m: nat):
forall acc,
execute_n_instructions (expt_loop_instructions m) {|
    pc := 2;
    program := expt_program;
    locals := n :: m :: acc :: nil;
    stack := nil;
|} = {|
    pc := 14;
    program := expt_program;
    locals := n :: 0 :: expt_iter n m acc :: nil;
    stack := nil;
|}.
Proof. induction m as [| m' IHm' ]; intros acc.
    - simpl. reflexivity.
    - rewrite evaluate_one_loop.
        simpl (S m' - 1).
        rewrite Nat.sub_0_r.
        rewrite IHm'.
        reflexivity.
Qed.
    
(* acc is set to 1 after two instructions *)
Lemma expt_setup (n m : nat) : 
    execute_n_instructions 2 {|
        pc := 0;
        program := expt_program;
        locals := n :: m :: 0 :: nil;
        stack := nil
    |} = {|
        pc := 2;
        program := expt_program;
        locals := n :: m :: 1 :: nil;
        stack := nil
|}. Proof. reflexivity. Qed.

Theorem jvm_expt_correct (n m : nat) : read_acc (jvm_expt n m) = expt n m.
Proof.
    unfold jvm_expt.
    unfold expt_total_instructions.
    rewrite Nat.add_comm.
    rewrite execute_plus_instructions.
    rewrite expt_setup.
    rewrite jvm_expt_iter.
    unfold read_acc.
    unfold read. (* simpl to expt_iter n m 1 = expt n m due to reading of acc*) 
    apply expt_iter_equivalent.
Qed.

Theorem jvm_expt_halts (n m : nat) : fetch (jvm_expt n m) = halt.
Proof.
    unfold jvm_expt.
    unfold expt_total_instructions.
    rewrite Nat.add_comm.
    rewrite execute_plus_instructions.
    rewrite expt_setup.
    rewrite jvm_expt_iter.
    unfold fetch.
    unfold program.
    unfold pc.
    reflexivity.
Qed.