package inflection;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class InflectionTest_v1 {
 @Test
 public void testMatch() {
 Inflection inflection = new Inflection("abc", "ABC");
 assertTrue(inflection.match("abcd"));
 assertFalse(inflection.match("abce"));
 }

 @Test
 public void testReplace() {
 Inflection inflection = new Inflection("abc", "ABC");
 assertEquals("ABCD", inflection.replace("abcd"));
 assertEquals("abce", inflection.replace("abce"));
 }

 @Test
 public void testPluralize() {
 assertEquals("apples", Inflection.pluralize("apple"));
 assertThrows(NullPointerException.class, () -> Inflection.pluralize[20D[K
Inflection.pluralize(null));
 }

 @Test
 public void testSingularize() {
 assertEquals("apple", Inflection.singularize("apples"));
 assertThrows(NullPointerException.class, () -> Inflection.singulari[20D[K
Inflection.singularize(null));
 }
}