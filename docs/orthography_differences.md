# Sesotho Orthography Differences

> **Exploratory linguistic notes.** The examples below are candidate patterns,
> not an independently reviewed prescriptive standard or a verified rule list.
> They must be checked by the primary collaborator and an independent Lesotho
> Sesotho reviewer before publication or rule freezing.

This document explains the key orthographic differences between South African Sesotho and Lesotho Sesotho, which are the focus of the SesoFix conversion tool.

## Background

Sesotho (Southern Sotho) is a Bantu language spoken primarily in South Africa and Lesotho. Despite being the same language, there are systematic orthographic (spelling) differences between the variants used in these two countries. These differences emerged due to separate standardization processes during the colonial period.

## Key Orthographic Differences

The main differences between South African Sesotho and Lesotho Sesotho orthography are:

### 1. Consonant Representation

| South African | Lesotho | Example (SA → LS) |
|---------------|---------|-------------------|
| `d` | `l` | `dibuka` → `libuka` (books) |
| `kg` | `kh` | `kgomo` → `khomo` (cow) |
| `tjh` | `ch` | `tjhaba` → `chaba` (nation) |
| `ph` | `ph` | (same in both) |
| `th` | `th` | (same in both) |

### 2. Vowel Sequences

| South African | Lesotho | Example (SA → LS) |
|---------------|---------|-------------------|
| `oa` | `oa` | (same in both) |
| `ea` | `ea` | (same in both) |
| `ya` | `ea` | `ya` → `ea` (goes) |

### 3. Demonstratives and Pronouns

| South African | Lesotho | Example (SA → LS) |
|---------------|---------|-------------------|
| `o` | `u` | `o phela joang` → `u phela joang` (how are you) |

### 4. Contractions

| South African | Lesotho | Example (SA → LS) |
|---------------|---------|-------------------|
| `ke a` | `kea` | `ke a leboga` → `kea leboha` (thank you) |

### 5. Other Common Patterns

| South African | Lesotho | Example (SA → LS) |
|---------------|---------|-------------------|
| `phodile` | `pholile` | `metsi a phodile` → `metsi a pholile` (the water is cold) |

## Examples of Conversion

Here are some complete sentence examples showing the conversion from South African to Lesotho orthography:

1. **South African**: Ke rata ho bala dibuka.  
   **Lesotho**: Ke rata ho bala libuka.  
   (I like to read books.)

2. **South African**: O ya kae?  
   **Lesotho**: U ea kae?  
   (Where are you going?)

3. **South African**: Ke nako ya ho ja.  
   **Lesotho**: Ke nako ea ho ja.  
   (It's time to eat.)

4. **South African**: Letsatsi le a tjhaba.  
   **Lesotho**: Letsatsi lea chaba.  
   (The sun is rising.)

5. **South African**: Ke a leboga.  
   **Lesotho**: Kea leboha.  
   (Thank you.)

## Challenges in Orthography Conversion

While many orthographic differences follow systematic patterns, there are several challenges in automatic conversion:

1. **Context-dependent changes**: Some conversions depend on the linguistic context.

2. **Exceptions to rules**: Not all patterns apply universally.

3. **Compound words**: Words formed by combining multiple roots may have special conversion rules.

4. **Loanwords**: Words borrowed from other languages may follow different orthographic conventions.

5. **Dialectal variations**: There are dialectal variations within both South African and Lesotho Sesotho.

## Why Neural Machine Translation Approach

Due to these challenges, a simple rule-based approach to orthography conversion may not be sufficient. The neural machine translation approach used in SesoFix can learn these patterns from data, including exceptions and context-dependent changes.

The ByT5 model, which operates at the byte level, is particularly well-suited for this task as it can capture character-level transformations without requiring specialized tokenization.

## References

For more information on Sesotho orthography:

1. Doke, C. M., & Mofokeng, S. M. (1957). Textbook of Southern Sotho Grammar. Longmans, Green.

2. Machobane, M., & Mokitimi, M. (1998). Problems in the Development of Sesotho Orthography. African Languages and Cultures, 11(2), 146-155.

3. Sesotho Online: [https://sesotho.org/](https://sesotho.org/)
