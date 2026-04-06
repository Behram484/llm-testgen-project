package camelcaseutil;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

public class CamelCaseUtilTest {
 
 @Test
 public void testFromCamelCase() {
 assertEquals("hello-world", CamelCaseUtil.fromCamelCase("HelloWorld[39D[K
CamelCaseUtil.fromCamelCase("HelloWorld"));
 assertEquals("this-is-a-test", CamelCaseUtil.fromCamelCase("ThisIsA[36D[K
CamelCaseUtil.fromCamelCase("ThisIsATest"));
 assertEquals("multi-word-string", CamelCaseUtil.fromCamelCase("Mult[33D[K
CamelCaseUtil.fromCamelCase("MultiWordString"));
 }
 
 @Test
 public void testFromCamelCaseWithCustomDelimiter() {
 assertEquals("hello_world", CamelCaseUtil.fromCamelCase("HelloWorld[39D[K
CamelCaseUtil.fromCamelCase("HelloWorld", '_'));
 assertEquals("this_is_a_test", CamelCaseUtil.fromCamelCase("ThisIsA[36D[K
CamelCaseUtil.fromCamelCase("ThisIsATest", '_'));
 assertEquals("multi_word_string", CamelCaseUtil.fromCamelCase("Mult[33D[K
CamelCaseUtil.fromCamelCase("MultiWordString", '_'));
 }
 
 @Test
 public void testNormalizeCamelCase() {
 assertEquals("helloWorld", CamelCaseUtil.normalizeCamelCase("HelloW[40D[K
CamelCaseUtil.normalizeCamelCase("HelloWorld"));
 assertEquals("thisIsATest", CamelCaseUtil.normalizeCamelCase("ThisI[39D[K
CamelCaseUtil.normalizeCamelCase("ThisIsATest"));
 assertEquals("multiWordString", CamelCaseUtil.normalizeCamelCase("M[35D[K
CamelCaseUtil.normalizeCamelCase("MultiWordString"));
 }
 
 @Test
 public void testToCamelCase() {
 assertEquals("helloWorld", CamelCaseUtil.toCamelCase("hello-world")[40D[K
CamelCaseUtil.toCamelCase("hello-world"));
 assertEquals("thisIsATest", CamelCaseUtil.toCamelCase("this-is-a-te[39D[K
CamelCaseUtil.toCamelCase("this-is-a-test"));
 assertEquals("multiWordString", CamelCaseUtil.toCamelCase("multi-wo[35D[K
CamelCaseUtil.toCamelCase("multi-word-string"));
 }
 
 @Test
 public void testToCamelCaseWithCustomDelimiter() {
 assertEquals("hello_world", CamelCaseUtil.toCamelCase("hello_world"[39D[K
CamelCaseUtil.toCamelCase("hello_world", '_'));
 assertEquals("this_is_a_test", CamelCaseUtil.toCamelCase("this_is_a[36D[K
CamelCaseUtil.toCamelCase("this_is_a_test", '_'));
 assertEquals("multi_word_string", CamelCaseUtil.toCamelCase("multi_[33D[K
CamelCaseUtil.toCamelCase("multi_word_string", '_'));
 }
}