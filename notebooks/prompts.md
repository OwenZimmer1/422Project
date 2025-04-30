
```py
zeroShot = PromptTemplate(
    input_variables=["method_code"],
    template='''\
Write a professional Javadoc comment for the following Java method. Only tell me the javadoc, **do not return any code**

Method:
{method_code}

Javadoc:
'''
)
```

```py
from langchain import PromptTemplate

oneShot = PromptTemplate(
    input_variables=["method_code"],
    template='''\
Write a professional Javadoc comment for the following Java method. Only tell me the javadoc, **do not return any code.** 

Example 1:
Method:
public String reverseProcessed(String text) {{
    if (text == null) return null;
    String cleaned = text.trim().toLowerCase();
    return new StringBuilder(cleaned).reverse().toString();
}}

Javadoc:
/**
 * Reverses the characters in the given string after trimming whitespace and converting to lowercase.
 *
 * @param text the input string to process
 * @return the reversed, lowercase, trimmed string
 */

Example 2:
Method:
private int add(int a, int b) {{
    return a + b;
}}

Javadoc:
/**
 * Adds two integers.
 *
 * @param a the first integer
 * @param b the second integer
 * @return the sum of the two integers
 */

Now write a Javadoc comment for this method:
Method:
{method_code}

Javadoc:
'''
)
```