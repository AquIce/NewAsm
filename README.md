# NewAsm

NewAsm is a little "recreation" of assembly language to train boolean logic and arithmetic.

## Environment

**NewAsm** is written in Python, and uses a custom interpreter to run the code.
> **Note :** All the datas are stored in a dictionary, and the code stack is stored in a list.

## Syntax

### Comments

Comments are written with `:` and are ignored by the interpreter.
Multiple lines comments are not allowed, but you can use multiple `:`.

### Memory Access

#### get

The `get` command is used to **get a view of the registry**.

The syntax is `get`.
> Note : This does not show the system registers values.

#### reg

The `reg` command is used to **add a value to the registry**.
The syntax is `reg <address> <value>`.
##### address

The field `address` is the address of the register.
It is in hexadecimal, and can be between `0x000010` and `0xfffff`.
> Note : The addresses `0x00000` to `0x00000f` are reserved for the system.

##### value

The field `value` is the value to add to the registry.
It can be :
- A binary value (0 or 1)
- A valid memory address (0x000000 to 0xfffff)
- An operation ([see below](#Operations))
> Note : An address is considered valid if it **is not** in the registry yet.

> Note : The addresses `0x00000` to `0x00000f` are reserved for the system.

##### Example :

```
: We put the value 0 in the register 0x000010
reg 0x000010 0
: We put the value of in the register 0x000011
reg 0x000011 0x000010
: We put the result of a NAND operation between 0x000010 and 0x000011 in the register 0x000012
reg 0x000012 nnd 0x000010 0x000011
: We show the registry
get
```

Output :

```
[NewAsm:(get):cout] >> {'0x000010': 0, '0x000011': 0, '0x000012': 1}
```

#### upt

The `upt` command is used to **update an existing value in the registry**.
The syntax is `upt <address> <value>`.
##### address

The field `address` is the address of the register.
It is in hexadecimal, and can be between `0x000010` and `0xfffff`.
> Note : The addresses `0x00000` to `0x00000f` are reserved for the system.

##### value

The field `value` is the value to update in the registry.
It can be :
- A binary value (0 or 1)
- A valid memory address (0x000000 to 0xfffff)
- A basic operation ([see below](###Basic-Operations)) or an advanced operation ([see below](###Advanced-Operations))
> Note : An address is considered valid if it **is** already in the registry.

> Note : The addresses `0x00000` to `0x00000f` are reserved for the system.

##### Example :

```
: We put the value 0 in the register 0x000010
reg 0x000010 0
: We put the value 1 in the register 0x000011
reg 0x000011 1
: We put the value 0 in the register 0x000012
reg 0x000012 0
: We show the registry
get
: We update the value of the register 0x000010 to 1
upt 0x000010 1
: We show the registry
get
: We update the value of the register 0x000011 to the value of the register 0x000010
upt 0x000011 0x000010
: We show the registry
get
: We put the value of the result of a NAND operation between 0x000010 and 0x000011 in the register 0x000012
upt 0x000012 nnd 0x000010 0x000011
: We show the registry
get
```

Output :

```
[NewAsm:(get):cout] >> {'0x000010': 0, '0x000011': 1, '0x000012': 0}
[NewAsm:(get):cout] >> {'0x000010': 1, '0x000011': 1, '0x000012': 0}
[NewAsm:(get):cout] >> {'0x000010': 1, '0x000011': 1, '0x000012': 0}
[NewAsm:(get):cout] >> {'0x000010': 1, '0x000011': 1, '0x000012': 0}
```

#### mov

The `mov` command is used to **move a value from a register to another** (the source register no longer exists).
The syntax is `mov <address1> <address2>`.

##### address1

The field `address1` is the address of the register to move.
It is a valid hexadecimal address, and can be between `0x000010` and `0xfffff`.
> Note : An address is considered valid if it **is** already in the registry.

> Note : The addresses `0x00000` to `0x00000f` are reserved for the system.

##### address2

The field `address2` is the address of the register to move to.
It is an hexadecimal address, and can be between `0x000010` and `0xfffff`.

> Note : The addresses `0x00000` to `0x00000f` are reserved for the system.

##### Example :

```
: We put the value 0 in the register 0x000010
reg 0x000010 0
: We show the registry
get
: We move the value of the register 0x000010 to the register 0x000011
mov 0x000010 0x000011
: We show the registry
get
```

Output :

```
[NewAsm:(get):cout] >> {'0x000010': 0}
[NewAsm:(get):cout] >> {'0x000011': 0}
```

#### cpy

The `cpy` command is used to **copy a value from a register to another** (the source register still exists).
The syntax is `cpy <address1> <address2>`.

##### address1

The field `address1` is the address of the register to copy.
It is a valid hexadecimal address, and can be between `0x000010` and `0xfffff`.
> Note : An address is considered valid if it **is** already in the registry.

> Note : The addresses `0x00000` to `0x00000f` are reserved for the system.

##### address2

The field `address2` is the address of the register to copy to.
It is an hexadecimal address, and can be between `0x000010` and `0xfffff`.
> Note : The addresses `0x00000` to `0x00000f` are reserved for the system.

##### Example :

```
: We put the value 0 in the register 0x000010
reg 0x000010 0
: We show the registry
get
: We copy the value of the register 0x000010 to the register 0x000011
cpy 0x000010 0x000011
: We show the registry
get
```

Output :

```
[NewAsm:(get):cout] >> {'0x000010': 0}
[NewAsm:(get):cout] >> {'0x000010': 0, '0x000011': 0}
```

#### del

The `del` command is used to **delete a register**.
The syntax is `del <address>`.

##### address

The field `address` is the address of the register to delete.
It is a valid hexadecimal address, and can be between `0x000010` and `0xfffff`.
> Note : An address is considered valid if it **is** already in the registry.

> Note : The addresses `0x00000` to `0x00000f` are reserved for the system.

##### Example :

```
: We put the value 0 in the register 0x000010
reg 0x000010 0
: We show the registry
get
: We delete the register 0x000010
del 0x000010
: We show the registry
get
```

Output :

```
[NewAsm:(get):cout] >> {'0x000010': 0}
[NewAsm:(get):cout] >> {}
```

### Basic Operations

The operations are used to **perform an operation between two (or more) values**.

#### nnd

The `nnd` operation is used to **perform a NAND operation** between two values.

##### Truthtable

| A | B | A NAND B |
|---|---|----------|
| 0 | 0 | 1        |
| 0 | 1 | 1        |
| 1 | 0 | 1        |
| 1 | 1 | 0        |

##### Syntax

The syntax is `nnd <value1> <value2>`.

##### value1

The field `value1` is the first value to use.
It can be a valid hexadecimal address or a binary value.
> Note : An address is considered valid if it **is** already in the registry.

##### value2

The field `value2` is the second value to use.
It can be a valid hexadecimal address or a binary value.
> Note : An address is considered valid if it **is** already in the registry.

##### Example :

```
: We put the value 0 in the register 0x000010
reg 0x000010 0
: We show the result of the NAND operation between 0x000010 and 1
eva nnd 0x000010 1
```
For more informations about eva : [Documentation for eva](####eva)

Output :

```
[NewAsm:(eva):cout] >> 1
```

#### not

The `not` operation is used to **perform a NOT operation** between two values.

##### Truthtable

| A | NOT A |
|---|-------|
| 0 | 1     |
| 1 | 0     |

##### Syntax

The syntax is `not <value>`.
The value is evaluated and the result is output.

##### value

The field `value` is the value to use.
It can be a valid hexadecimal address or a binary value.
> Note : An address is considered valid if it **is** already in the registry.

##### Example :

```
: We put the value 0 in the register 0x000010
reg 0x000010 0
: We show the result of the NOT operation on 0x000010
eva not 0x000010
```
For more informations about eva : [Documentation for eva](####eva)

Output :

```
[NewAsm:(eva):cout] >> 1
```

##### Logic Gates

`NOT(A)` is the same as `NAND(A, A)`.
See [NAND](####nnd) for more informations.

#### and

The `and` operation is used to **perform a AND operation** between two values.

##### Truthtable

| A | B | A AND B |
|---|---|---------|
| 0 | 0 | 0       |
| 0 | 1 | 0       |
| 1 | 0 | 0       |
| 1 | 1 | 1       |

##### Syntax

The syntax is `and <value1> <value2>`.
The value is evaluated and the result is output.

##### value1

The field `value1` is the first value to use.
It can be a valid hexadecimal address or a binary value.
> Note : An address is considered valid if it **is** already in the registry.

##### value2

The field `value2` is the second value to use.
It can be a valid hexadecimal address or a binary value.
> Note : An address is considered valid if it **is** already in the registry.

##### Example :

```
: We put the value 0 in the register 0x000010
reg 0x000010 0
: We show the result of the AND operation between 0x000010 and 1
eva and 0x000010 1
```

Output :

```
[NewAsm:(eva):cout] >> 0
```

##### Logic Gates

`AND(A, B)` is the same as `NOT(NAND(A, B))`.
See [NAND](####nnd) and [NOT](####not) for more informations.

#### or

The `or` operation is used to **perform a OR operation** between two values.

##### Truthtable

| A | B | A OR B |
|---|---|--------|
| 0 | 0 | 0      |
| 0 | 1 | 1      |
| 1 | 0 | 1      |
| 1 | 1 | 1      |

##### Syntax

The syntax is `or <value1> <value2>`.
The value is evaluated and the result is output.

##### value1

The field `value1` is the first value to use.
It can be a valid hexadecimal address or a binary value.
> Note : An address is considered valid if it **is** already in the registry.

##### value2

The field `value2` is the second value to use.
It can be a valid hexadecimal address or a binary value.
> Note : An address is considered valid if it **is** already in the registry.

##### Example :

```
: We put the value 0 in the register 0x000010
reg 0x000010 0
: We show the result of the OR operation between 0x000010 and 1
eva or 0x000010 1
```

Output :

```
[NewAsm:(eva):cout] >> 1
```

##### Logic Gates

`OR(A, B)` is the same as `NAND(NOT(A), NOT(B))`.
See [NAND](####nnd) and [NOT](####not) and for more informations.

### Advanced Operations

The advanced operations are used to **perform an operation between two (or more) values**.

#### xor

The `xor` operation is used to **perform a XOR operation** between two values.

##### Truthtable

| A | B | A XOR B |
|---|---|---------|
| 0 | 0 | 0       |
| 0 | 1 | 1       |
| 1 | 0 | 1       |
| 1 | 1 | 0       |

##### Syntax

The syntax is `xor <value1> <value2>`.
The value is evaluated and the result is output.

##### value1

The field `value1` is the first value to use.
It can be a valid hexadecimal address or a binary value.
> Note : An address is considered valid if it **is** already in the registry.

##### value2

The field `value2` is the second value to use.
It can be a valid hexadecimal address or a binary value.
> Note : An address is considered valid if it **is** already in the registry.

##### Example :

```
: We put the value 0 in the register 0x000010
reg 0x000010 0
: We show the result of the XOR operation between 0x000010 and 1
eva xor 0x000010 1
```

Output :

```
[NewAsm:(eva):cout] >> 1
```

##### Logic Gates

`XOR(A, B)` is the same as `AND(OR(A, B), NAND(A, B))`.
See [NAND](####nnd), [AND](####and) and [OR](####or) for more informations.

### Special commands

#### eva

The `eva` command is used to **evaluate a value**.
The syntax is `eva <value>`.
The value is evaluated and the result is output.

##### value

The field `value` is the value to evaluate.
It can be a valid hexadecimal address, a binary value or even the result of an [operation](###Operations).
> Note : An address is considered valid if it **is** already in the registry.

##### Example :

```
: We put the value 0 in the register 0x000010
reg 0x000010 1
: We show the result of the NAND operation between 0x000010 and 1
eva nnd 0x000010 1
```

Output :

```
[NewAsm:(eva):cout] >> 0
```