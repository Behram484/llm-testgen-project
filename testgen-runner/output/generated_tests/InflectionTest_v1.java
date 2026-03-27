package inflection;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

class InflectionTest_v1 {
 
 // Passing tests (keep unchanged)
 @Test
 void testIsUncountable() {
 assertTrue(Inflection.isUncountable("rice"));
 assertFalse(Inflection.isUncountable("apple"));
 }
 
 @Test
 void testPluralize() {
 assertEquals("people", Inflection.pluralize("person"));
 assertThrows(NullPointerException.class, () -> Inflection.pluralize(null));
 }
 
 // Failing test methods 
 @Test
 void testSingularize() {
 assertEquals("child", Inflection.singularize("children"));
 assertThrows(NullPointerException.class, () -> Inflection.singularize(null));
 }
}