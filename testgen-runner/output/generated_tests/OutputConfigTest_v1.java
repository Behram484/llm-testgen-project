package outputconfig;

import java.util.*;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

class OutputConfigTest_v1 {
 @Test
 void testCreateOutputConfig() {
 Properties props = new Properties();
 props.setProperty("method", "xml");
 props.setProperty("version", "1.0");
 props.setProperty("encoding", "UTF-8");
 props.setProperty("omit_xml_declaration", "no");
 props.setProperty("standalone", "yes");
 props.setProperty("doctype_public", "-//W3C//DTD XHTML 1.0 Strict//EN");
 props.setProperty("doctype_system", "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd");
 props.setProperty("cdata_section_elements", "script java");
 props.setProperty("indent", "yes");
 props.setProperty("media_type", "text/html");
 
 OutputConfig output = OutputConfig.createOutputConfig(props);
 
 assertEquals("xml", output.method);
 assertFalse(output.isXhtml);
 assertFalse(output.isText);
 assertFalse(output.isHtml);
 assertEquals("1.0", output.version);
 assertEquals("UTF-8", output.encoding);
 assertEquals(0, output.omit_xml_declaration);
 assertTrue(output.standalone);
 assertEquals("-//W3C//DTD XHTML 1.0 Strict//EN", output.doctype_public);
 assertEquals("http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd", output.doctype_system);
 assertTrue(output.cdata_section_elements.containsAll(Arrays.asList("script", "java")));
 assertTrue(output.indent);
 assertEquals("text/html", output.media_type);
 }
}