package filtermatcher;

import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

public class FilterMatcherTest {
 private FilterMatcher filterMatcher;

 @BeforeEach
 public void setUp() {
 filterMatcher = new FilterMatcher("Geer%", null);
 }

 // Passing tests
 @Test
 public void testGetMetaDataMatchString() {
 assertEquals("Geer%", filterMatcher.getMetaDataMatchString());
 }

 @Test
 public void testGetSqlLikeMatchString() {
 assertTrue(filterMatcher.getSqlLikeMatchString().equals("%") || filterMatcher.getSqlLikeMatchString().equals("Geer%"));
 }

 @Test
 public void testMatchesWithExcludedPatternNonMatchingObjectName() {
 assertFalse(filterMatcher.matches("Alice"));
 }

 // Failing test with correct assertion
 @Test
 public void testMatchesWithIncludedPatternMatchingObjectName() {
 assertTrue(filterMatcher.matches("Gerhard")); // Changed to assertTrue since the method should return true for a matching pattern
 }

 // New failing tests targeted at surviving mutants: matchesPatterns
 @Test
 public void testGetMetaDataMatchStringWithNoIncludePattern() {
 filterMatcher = new FilterMatcher(null, "Geer%");
 assertNull(filterMatcher.getMetaDataMatchString()); // No include pattern should return null
 }

 @Test
 public void testGetSqlLikeMatchStringWithNoIncludePattern() {
 filterMatcher = new FilterMatcher(null, "Geer%");
 assertEquals("%", filterMatcher.getSqlLikeMatchString()); // No include pattern should return wildcard %
 }
}