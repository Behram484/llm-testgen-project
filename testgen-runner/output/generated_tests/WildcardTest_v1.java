package wildcard;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class WildcardTest_v1 {
 private final Wildcard w = new Wildcard(); // create an instance of th[2D[K
the Wildcard for method calls
 
 @Test
 void testIsWildcard() {
 // Test when pattern contains '*'
 assertTrue(Wildcard.isWildcard("*.txt"));
 
 // Test when pattern contains ';'
 assertTrue(Wildcard.isWildcard("file1.*;file2.*"));
 
 // Test when pattern does not contain '*' or ';'
 assertFalse(Wildcard.isWildcard("filename"));
 }
 
 @Test
 void testMatchWildcard() {
 // Test when filename matches the wildcard pattern
 assertEquals("file.txt", Wildcard.matchWildcard("*.txt", "file.txt"[10D[K
"file.txt"));
 
 // Test when filename does not match the wildcard pattern
 assertNull(Wildcard.matchWildcard("*.jpg", "file.txt"));
 }
 
 @Test
 void testInstantiateWildcard() {
 // Test instantiation of wildcard pattern with a part
 assertEquals("file.txt", Wildcard.instantiateWildcard("*.txt", "fil[4D[K
"file.txt"));
 
 // Test instantiation of wildcard pattern without substitution
 assertEquals("*.txt", Wildcard.instantiateWildcard("*.txt", ""));
 }
}