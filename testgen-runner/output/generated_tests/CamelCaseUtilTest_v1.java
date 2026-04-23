package camelcaseutil;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class CamelCaseUtilTest_v1 {
 @Test
 void testFromCamelCaseWithDefaultDelimiter() {
 assertEquals("hello-world", CamelCaseUtil.fromCamelCase("HelloWorld"));
 }

 @Test
 void testFromCamelCaseWithCustomDelimiter() {
 assertEquals("hello_world", CamelCaseUtil.fromCamelCase("HelloWorld", '_[2D[K
'_'));
 }

 @Test
 void testNormalizeCamelCase() {
 assertEquals("helloWorld", CamelCaseUtil.normalizeCamelCase("helloW"));
 assertEquals("hello_world", CamelCaseUtil.normalizeCamelCase("hello_worl[44D[K
CamelCaseUtil.normalizeCamelCase("hello_world"));
 assertEquals("HelloWorld", CamelCaseUtil.normalizeCamelCase("HelloWorld"[45D[K
CamelCaseUtil.normalizeCamelCase("HelloWorld"));
 }

 @Test
 void testToCamelCaseWithDefaultDelimiter() {
 assertEquals("helloWorld", CamelCaseUtil.toCamelCase("hello-world"));
 }

 @Test
 void testToCamelCaseWithCustomDelimiter() {
 assertEquals("helloWorld", CamelCaseUtil.toCamelCase("hello_world", '_'[3D[K
'_'));
 }
}