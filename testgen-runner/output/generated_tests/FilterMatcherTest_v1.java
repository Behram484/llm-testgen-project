package filtermatcher;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.regex.PatternSyntaxException;

public class FilterMatcherTest_v1 {
 @Test
 void testFilterMatcher() throws PatternSyntaxException{
 FilterMatcher filterMatcher = new FilterMatcher("Geer%", null);
 
 assertEquals(filterMatcher.getMetaDataMatchString(), "Geer%");
 assertThrows(PatternSyntaxException.class, () -> filterMatcher.new Filt[4D[K
FilterMatcher("%^&\\[18D\\]\[KFilterMatcher(\"%^&*", null));
 }
 
 @Test
 void testMatches() {
 FilterMatcher filterMatcher = new FilterMatcher("Geer%", "Geri");
 
 assertEquals(filterMatcher.matches("Georgetown"), true);
 assertEquals(filterMatcher.matches("Gerhard"), false);
 }
 
 @Test
 void testGetMetaDataMatchString() {
 FilterMatcher filterMatcher = new FilterMatcher("Geer%", null);
 
 assertEquals(filterMatcher.getMetaDataMatchString(), "Geer%");
 }
 
 @Test
 void testGetSqlLikeMatchString() {
 FilterMatcher filterMatcher1 = new FilterMatcher("Geer%", null);
 
 assertEquals(filterMatcher1.getSqlLikeMatchString(), "Geer%");
 
 FilterMatcher filterMatcher2 = new FilterMatcher(null, null);
 assertEquals(filterMatcher2.getSqlLikeMatchString(), "%");
 }
}