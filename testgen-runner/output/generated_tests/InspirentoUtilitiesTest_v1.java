package com.allenstudio.ir.util;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class InspirentoUtilitiesTest_v1 {
 @Test
 void testTokenize() {
 String[] expected = {"file", "edit", "view"};
 assertArrayEquals(expected, InspirentoUtilities.tokenize("file edit vie[3D[K
view"));
 
 String delim = "-";
 assertArrayEquals(expected, InspirentoUtilities.tokenize("file-edit-vie[43D[K
InspirentoUtilities.tokenize("file-edit-view", delim));
 }

 @Test
 void testEscapeText() {
 String expected = "This &amp; That &gt; These";
 assertEquals(expected, InspirentoUtilities.escapeText("This & That > Th[2D[K
This"));
 
 // Test with special characters
 expected = "&lt;&lt; &amp;quot;This is a test&amp;quot; &amp;gt; &amp;l[6D[K
&amp;lt; That";
 assertEquals(expected, InspirentoUtilities.escapeText("<< \"This is a t[1D[K
test\" >> & This < That"));
 }
}