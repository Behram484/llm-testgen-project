package wildcard;

import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.Test;

class WildcardTest_v1 {
 @Test
 void testInstantiateWildcard() {
 assertEquals("", Wildcard.instantiateWildcard("prefix*suffix", ""));
 assertEquals("t_sted", Wildcard.instantiateWildcard("t*sted", "_"));
 }

 @Test
 void testMatchWildcard() {
 assertNull(Wildcard.matchWildcard("prefix*suffix", "test"));
 assertNull(Wildcard.matchWildcard("t*sted", "ested"));
 }

 // Copy these EXACTLY into your output, do not modify them
 @Test
 void testIsWildcard() {
 assertTrue(Wildcard.isWildcard("*"));
 assertFalse(Wildcard.isWildcard("test"));
 }
}