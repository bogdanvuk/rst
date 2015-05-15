/*
 * generated by Xtext
 */
package rs.demsys.rst.formatting2;

import org.eclipse.xtext.ui.editor.model.IXtextDocument;
import com.google.inject.Inject;
import org.eclipse.xtext.formatting2.AbstractFormatter2;
import org.eclipse.xtext.formatting2.IFormattableDocument;
import rs.demsys.rst.rst.Block;
import rs.demsys.rst.rst.DirectiveOption;
import rs.demsys.rst.rst.Document;
import rs.demsys.rst.rst.ImageDirective;
import rs.demsys.rst.rst.LatexLine;
import rs.demsys.rst.rst.Literal;
import rs.demsys.rst.rst.MathDirective;
import rs.demsys.rst.rst.OtherDirective;
import rs.demsys.rst.rst.Paragraph;
import rs.demsys.rst.rst.Replacement;
import rs.demsys.rst.rst.Section;
import rs.demsys.rst.rst.Text;
import rs.demsys.rst.rst.TextLine;
import rs.demsys.rst.services.RstGrammarAccess;
import rs.demsys.rst.rst.Heading
import org.eclipse.xtext.nodemodel.util.NodeModelUtils
import org.eclipse.emf.ecore.EObject
import java.util.List
import org.eclipse.xtext.EcoreUtil2
import org.eclipse.xtext.resource.XtextResource
import org.eclipse.xtext.util.concurrent.IUnitOfWork
import rs.demsys.rst.formatting2.RstFormatterHelper

class RstFormatter extends AbstractFormatter2 {
	
	@Inject extension RstGrammarAccess

	def dispatch void format(Document doc, extension IFormattableDocument document) {
		// TODO: format HiddenRegions around keywords, attributes, cross references, etc. 
		
		for (Section section : doc.getSection()) {
			format(section, document);
		}
	}

	def dispatch void format(Replacement replacement, extension IFormattableDocument document) {
		// TODO: format HiddenRegions around keywords, attributes, cross references, etc. 
		format(replacement.getText(), document);
	}
	
	def dispatch void format(Heading heading, extension IFormattableDocument document) {
		// TODO: format HiddenRegions around keywords, attributes, cross references, etc.

	}

//	def dispatch void format(Paragraph paragraph, extension IFormattableDocument document) {
//		// TODO: format HiddenRegions around keywords, attributes, cross references, etc. 
//		for (TextLine line : paragraph.getLine()) {
//			format(line, document);
//		}
//	}

	def dispatch void format(Block block, extension IFormattableDocument document) {
		// TODO: format HiddenRegions around keywords, attributes, cross references, etc. 
		for (DirectiveOption options : block.getOptions()) {
			format(options, document);
		}
		for (Section sec : block.getBlock()) {
			format(sec, document);
		}
	}

	def dispatch void format(MathDirective mathdirective, extension IFormattableDocument document) {
		// TODO: format HiddenRegions around keywords, attributes, cross references, etc. 
		for (DirectiveOption options : mathdirective.getOptions()) {
			format(options, document);
		}
		for (LatexLine block : mathdirective.getBlock()) {
			format(block, document);
		}
	}

	def dispatch void format(ImageDirective imagedirective, extension IFormattableDocument document) {
		// TODO: format HiddenRegions around keywords, attributes, cross references, etc. 
		format(imagedirective.getBlock(), document);
	}

	def dispatch void format(OtherDirective otherdirective, extension IFormattableDocument document) {
		// TODO: format HiddenRegions around keywords, attributes, cross references, etc. 
		format(otherdirective.getBlock(), document);
	}

	def dispatch void format(TextLine textline, extension IFormattableDocument document) {
		// TODO: format HiddenRegions around keywords, attributes, cross references, etc. 
		format(textline.getFirst(), document);
		format(textline.getText(), document);
	}

	def dispatch void format(Text text, extension IFormattableDocument document) {
		// TODO: format HiddenRegions around keywords, attributes, cross references, etc. 
		for (Literal items : text.getItems()) {
			format(items, document);
		}
	}
}
