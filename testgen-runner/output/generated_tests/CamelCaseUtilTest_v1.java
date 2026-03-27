package camelcaseutil;

import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.Test;

class CamelCaseUtilTest_v1 {
 @Test
 void testNormalizeCamelCase() {
 String input = "camelCASE";
 String expectedOutput = "camel case";
 
 assertEquals(expectedOutput, CamelCaseUtil.normalizeCamelCase(input));
 }
}