---
title: "Going Deeper"
description: ""
author: ""
date: 2025-12-18T06:19:13-05:00
subtitle: ""
image: ""
post-tags: []
posts: []
draft: false
---

I want to understand my field from absolute --- not quite going back to the
start of the universe --- first principles. I've read George Boole's _The Mathematical
Analysis of Logic_ and have _An Investigation of the Laws of Thought: On which are founded the mathematical theories of logic
and probabilities_.

Let's do a bit of "top down" and then we'll do some "bottom up" in another
post.

```rust
fn main() {
    println!("hello")
}
```

What's the machine code?

Maybe start with `cargo build` and `hexdump`?

```txt
# 227133 lines!
0000000 457f 464c 0102 0001 0000 0000 0000 0000
0000010 0003 003e 0001 0000 7930 0000 0000 0000
0000020 0040 0000 0000 0000 64c0 0038 0000 0000
0000030 0000 0000 0040 0038 000e 0040 0029 0028
...
0386ee0 018b 0000 0000 0000 0000 0000 0000 0000
0386ef0 0001 0000 0000 0000 0000 0000 0000 0000
0386f00
```

Let's use the wikipedia of this generation, AI, to understand.

First, it tells me if I'm interested in the assembly or machine
code, just running `hexdump` is wrong. Cool, so then what
is this showing?

> hexdump gives you the raw bytes but doesn’t preserve the structure you need for proper disassembly.

> Your hexdump is showing the raw bytes of the ELF binary in 16-bit little-endian groups.

Line 1 decodes to:
- `457f 464c` = `7f 45 4c 46` = ELF magic number (.ELF)
- `0102` = 64-bit, little-endian
- `0001` = current ELF version
- `003e` (line 2) = x86-64 architecture

The data includes:
- ELF headers and program headers
- .text section (actual machine code)
- .rodata, .data, .bss (data sections)
- Symbol tables, relocations, etc.

AI tells me to use `objdump -d -M intel -C your_binary > disassembly.asm`

```
-d              Disassemble executable sections
-D              Disassemble all sections
-M intel        Use Intel syntax (vs AT&T default)
-C              Demangle C++/Rust symbols
-S              Intermix source code (if compiled with -g)
-l              Include line numbers
--no-show-raw-insn  Hide hex bytes, just show assembly
-j .text        Disassemble only .text section
```

Oh wow, 68812 lines in this `disassembly.asm` file.

I mean I didn't _try_ to make a small binary. I didn't use `nostd` and
just ran `cargo build`, which I imagine leaves some debug symbols, etc. or
something.

Then AI suggests that I check out `cargo-show-asm` or `cargo llvm-ir` which would understand the Rust "mangling"
better and would enable looking at assembly for specific functions or the intermediate
LLVM representation. Eh we'll get here. I don't want to understand the Rust
specifics, yet.

AI also suggested these two references:
- https://www.felixcloutier.com/x86/
- Programming from the Ground Up: Bartlett, Jonathan, et. al.
    - This book is honestly EXACTLY what I was looking for. It is amazing.

I also just picked up https://eater.net/6502.

I don't want to just go minimal yet. I want to _try_ to understand a "normal"
program before I minimize or compile with specific flags.

# ELF (Executable and Linkable Format)

```
Offset  Field
0x00    Magic (7f 45 4c 46 = .ELF)
0x04    Class (01=32-bit, 02=64-bit)
0x05    Endianness (01=little, 02=big)
0x10    Type (02=executable, 03=shared object)
0x12    Machine (3e=x86-64, 28=ARM)
0x18    Entry point address (where execution starts)
0x20    Program header offset
0x28    Section header offset
```

```
0000000 457f 464c 0102 0001 0000 0000 0000 0000
0000010 0003 003e 0001 0000 7930 0000 0000 0000
0000020 0040 0000 0000 0000 64c0 0038 0000 0000
0000030 0000 0000 0040 0038 000e 0040 0029 0028
0000040 0006 0000 0004 0000 0040 0000 0000 0000
```

Why groups of 4 hex digits (2 bytes)?
    - Tool default for readability
	- Easier to spot patterns than single bytes
Why 8 groups (16 bytes) per line?
	- Convention: 16 bytes fits nicely on terminal

And AI tells me that the offset column is 7-hex-digits long only because
of the size of my binary which is 3.7MB and 7-digits is enough to represent
the address space of a binary of that size.

It's just a default display thing, but internally it's still using 64-bit addresses.
A 3.7MB file only needs 22 bits of addressing (2^22 = 4MB).

```bash
07:00:54 %% ls -al target/debug/app
-rwxr-xr-x 2 mccurdyc users 3698432 Dec 18 06:16 target/debug/app
```

# readelf -all target/debug/app

Okay, wow this is way more helpful.

```txt
# readelf -h ...
ELF Header:
  Magic:   7f 45 4c 46 02 01 01 00 00 00 00 00 00 00 00 00
  Class:                             ELF64
  Data:                              2's complement, little endian
  Version:                           1 (current)
  OS/ABI:                            UNIX - System V
  ABI Version:                       0
  Type:                              DYN (Position-Independent Executable file)
  Machine:                           Advanced Micro Devices X86-64
  Version:                           0x1
  Entry point address:               0x7930
  Start of program headers:          64 (bytes into file)
  Start of section headers:          3695808 (bytes into file)
  Flags:                             0x0
  Size of this header:               64 (bytes)
  Size of program headers:           56 (bytes)
  Number of program headers:         14
  Size of section headers:           64 (bytes)
  Number of section headers:         41
  Section header string table index: 40
```

# Let's start to minimize now

```
objdump -d -M intel -C target/debug/app > out/objdump-min.out
# still 68800 lines
```

```
07:37:16 %% grep -A5 -P '(?<!(driftsort_|thread::))main' out/objdump-min.out
    7948:       48 8d 3d 41 02 00 00    lea    rdi,[rip+0x241]        # 7b90 <main>
    794f:       ff 15 1b ff 04 00       call   QWORD PTR [rip+0x4ff1b]        # 57870 <__libc_start_main@GLIBC_2.34>
    7955:       f4                      hlt
    7956:       66 2e 0f 1f 84 00 00    cs nop WORD PTR [rax+rax*1+0x0]
    795d:       00 00 00

0000000000007960 <deregister_tm_clones>:
--
0000000000007b60 <app::main>:
    7b60:       48 83 ec 38             sub    rsp,0x38
    7b64:       48 8d 7c 24 08          lea    rdi,[rsp+0x8]
    7b69:       48 8d 35 a8 d2 04 00    lea    rsi,[rip+0x4d2a8]        # 54e18 <__do_global_dtors_aux_fini_array_entry+0x38>
    7b70:       e8 ab ff ff ff          call   7b20 <core::fmt::Arguments::new_const>
    7b75:       48 8d 7c 24 08          lea    rdi,[rsp+0x8]
--
0000000000007b90 <main>:
    7b90:       50                      push   rax
    7b91:       48 89 f2                mov    rdx,rsi
    7b94:       48 8d 05 7d 49 04 00    lea    rax,[rip+0x4497d]        # 4c518 <__rustc_debug_gdb_scripts_section__>
    7b9b:       8a 00                   mov    al,BYTE PTR [rax]
    7b9d:       48 63 f7                movsxd rsi,edi
    7ba0:       48 8d 3d b9 ff ff ff    lea    rdi,[rip+0xffffffffffffffb9]        # 7b60 <app::main>
    7ba7:       31 c9                   xor    ecx,ecx
    7ba9:       e8 02 ff ff ff          call   7ab0 <std::rt::lang_start>
    7bae:       59                      pop    rcx
    7baf:       c3                      ret
```

AI helps

```txt
_start (not shown)
  → __libc_start_main
    → main (0x7b90)
      → std::rt::lang_start
        → app::main (0x7b60)
```

This is Intel syntax assembly with objdump annotations. The `<...>` pieces are objdump annotations

And the machine code is in that second column.

So the CPU see `7b90: 50 48 89 f2 48 8d 05 7d 49 04 00 8a 00 48 63 f7 ...`.
Well not the `7b90` part. That's the memory address.

Variable-length encoding: x86-64 instructions are 1-15 bytes (typical is between 2-4 bytes).

Fetch, Decode, Execute loop:
1. Fetches bytes from memory
2. Determines instruction length by examining opcodes/prefixes
3. Executes that instruction
4. Advances instruction pointer (RIP) by that many bytes

# Understanding opcodes

- https://cdrdv2-public.intel.com/868137/325462-089-sdm-vol-1-2abcd-3abcd-4.pdf
- https://www.felixcloutier.com/x86/
- ref.x86asm.net/coder64.html

# Understanding `main`

```asm
0000000000007b60 <app::main>:
    7b60:	48 83 ec 38          	sub    rsp,0x38
    7b64:	48 8d 7c 24 08       	lea    rdi,[rsp+0x8]
    7b69:	48 8d 35 a8 d2 04 00 	lea    rsi,[rip+0x4d2a8]        # 54e18 <__do_global_dtors_aux_fini_array_entry+0x38>
    7b70:	e8 ab ff ff ff       	call   7b20 <core::fmt::Arguments::new_const>
    7b75:	48 8d 7c 24 08       	lea    rdi,[rsp+0x8]
    7b7a:	ff 15 a8 ff 04 00    	call   QWORD PTR [rip+0x4ffa8]        # 57b28 <_GLOBAL_OFFSET_TABLE_+0x350>
    7b80:	48 83 c4 38          	add    rsp,0x38
    7b84:	c3                   	ret
    7b85:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
    7b8c:	00 00 00 
    7b8f:	90                   	nop
```

```
    7b60:	48 83 ec 38          	sub    rsp,0x38
```

How does this machine code encode this instruction?

`48 83 ec 38` - subtract from the `rsp` register `0x38`

From AI:
1.	48 - REX.W prefix (indicates 64-bit operand size)
2.	83 - opcode for SUB with sign-extended 8-bit immediate
3.	ec - ModR/M byte
    - mod: 11 (register direct)
    - reg: 101 (SUB operation)
    - r/m: 100 (RSP register)
4.	38 - immediate value (0x38 = 56 decimal)


Okay, let's actually understand this:

https://www.felixcloutier.com/x86/sub

> opcode            | Instruction       | Op Encoding | ... | Description
> ...
> REX.W + 83 /5 ib	| SUB r/m64, imm8	| MI	      | ... | Subtract sign-extended imm8 from r/m64.
> ...

> Op Encoding   | Operand 1         | Operand 2  | ...
> MI            | ModRM:r/m (r, w)  | imm8/16/32 | ...

I get that we're subtracting 56 (decimal) from the stack pointer. Presumably for function arguments to `println` (which is a macro, so we know it's syntactic sugar) or something.

It might be time to minimize a bit. Or work more from bottom up to "meet in the middle". I think there are too many abstractions that I don't
yet understand to make "top down" understandable.

So we can work bottom up and then top down by using `no std` and not using macros.

# How does a microprocessor work?

I know we give it some input in the form of bits?

The input is destined to specific locations of the microprocessor (thinking
each "prong").

# What does a resistor do? How does it work?

My guess is that it's adding resistence (or control) to some
electrical voltage.

Ah, and you only need a resistor where the device you are sending a signal
doesn't limit or handle the input voltage e.g., an LED. AI says that most
integrated circuits are designed to handle the direct 5V input.

# Why is "high" or "on" 5V? Why not 9V? or 1V?

It actually isn't always 5V anymore.

Microcontrollers like the 6502 used 5V because, at the time, most support chips (static RAMs, ROMs,
peripheral were all built for 5V logic levels.
So a 5V CPU could interface with them directly without level shifting.

The "high" voltage also isn't totally arbitrary and is actually defined
by common standards for interface compatibility.

AI: Each logic family (TTL, CMOS, LVTTL, etc.) specifies a supply voltage
and then defines input thresholds: above some voltage (VIH) is read as
logic 1, below another (VIL) is logic 0, and anything in between is undefined.
