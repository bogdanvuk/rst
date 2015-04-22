package rs.demsys.rst.ui.highlighting;

import java.util.Iterator;
import java.util.List;

import rs.demsys.rst.rst.*;

import org.eclipse.emf.common.util.TreeIterator;
import org.eclipse.emf.ecore.EObject;
import org.eclipse.emf.ecore.EReference;
import org.eclipse.xtext.Keyword;
import org.eclipse.xtext.RuleCall;
import org.eclipse.xtext.impl.TerminalRuleImpl;
import org.eclipse.xtext.nodemodel.*;
import org.eclipse.xtext.nodemodel.impl.*;
import org.eclipse.xtext.nodemodel.util.NodeModelUtils;
import org.eclipse.xtext.resource.XtextResource;
import org.eclipse.xtext.ui.editor.syntaxcoloring.*;
import org.eclipse.xtext.util.PolymorphicDispatcher;
import org.eclipse.xtext.impl.RuleCallImpl;

import static rs.demsys.rst.ui.highlighting.RstHighlightingConfiguration.*;

public class RstHighlightingCalculator implements
        ISemanticHighlightingCalculator {
//    public void provideHighlightingFor(XtextResource resource,
//            IHighlightedPositionAcceptor acceptor) {
//        if (resource == null || resource.getContents().isEmpty())
//			return;
//        INode root = resource.getParseResult().getRootNode();
//        BidiTreeIterator<INode> it = root.getAsTreeIterable().iterator();
//
//        while (it.hasNext()) {
//        	INode node = it.next();
//        	
//        	if (node.hasDirectSemanticElement())
//        	{
//        		highlightingFor.invoke(node.getSemanticElement(), it, acceptor);
//        	}
//        	else
//        	{
//        		if (node.getGrammarElement() != null)
//        		{
//        			if (node.getGrammarElement() instanceof RuleCallImpl)
//        			{
//		        		RuleCallImpl ruleCall = (RuleCallImpl) node.getGrammarElement();
//		        		
//		        		String ruleName = ruleCall.getRule().getName();
//		        		
//		        		System.out.println(ruleName);
//		        		
//		        		if (ruleName.equals("Italic"))
//		        		{
//		        			acceptor.addPosition(node.getParent().getOffset(), node.getParent().getLength(),
//		                            ITALIC_TEXT);
//		        		} 
//		        		else if (ruleName.equals("Bold"))
//		        		{
//		        			acceptor.addPosition(node.getParent().getOffset(), node.getParent().getLength(),
//		                            BOLD_TEXT);
//		        		}
//        			}
//        		}
//        	}
//		}
                
//            INode node = it.next();
//            if (node instanceof CompositeNodeWithSemanticElement
//                    && node.getSemanticElement() instanceof Directive) {
//                setStyles(acceptor, it, DIRECTIVE, DIRECTIVE_TYPE, DIRECTIVE);
//            } else if (node instanceof CompositeNode
//                    && node.getSemanticElement() instanceof Heading)
//                    {
//                setStyles(acceptor, it, HEADING, HEADING);
//            }
//            else if( node instanceof HiddenLeafNode && node.getGrammarElement() instanceof TerminalRuleImpl )
//            {
//                TerminalRuleImpl ge = (TerminalRuleImpl) node.getGrammarElement();
//                if( ge.getName().equalsIgnoreCase( "BOLD" ) ) 
//                    acceptor.addPosition( node.getOffset(), node.getLength(), HEADING );
//            }
//        }
//    }
	
	public void provideHighlightingFor(final XtextResource resource, IHighlightedPositionAcceptor acceptor) {
		if (resource == null || resource.getContents().isEmpty())
			return;
		TreeIterator<EObject> iterator = resource.getAllContents();
		while (iterator.hasNext()) {
			EObject eObject = (EObject) iterator.next();
			INode node = NodeModelUtils.findActualNodeFor(eObject);
//			System.out.println(node.getText());
			highlightingFor.invoke(eObject, node, acceptor);
		}
	}
    
	private PolymorphicDispatcher<Void> highlightingFor = PolymorphicDispatcher.createForSingleTarget("highlight", 3, 3, this);

	protected void highlight(EObject obj, INode node, IHighlightedPositionAcceptor acceptor) {
		
	}

	protected void highlight(OtherDirective obj, INode node, IHighlightedPositionAcceptor acceptor) {
		Iterator<ILeafNode> leaves = node.getLeafNodes().iterator();
		while(leaves.hasNext())
		{
			ILeafNode n = leaves.next();
			acceptor.addPosition(n.getOffset(), n.getLength(), DIRECTIVE);
			
			if (n.getText().equals("::"))
				break;
		}
	}
	
//	protected void highlight(IncludeDirective obj, INode node, IHighlightedPositionAcceptor acceptor) {
//		Iterator<ILeafNode> leaves = node.getLeafNodes().iterator();
//		
//		while(leaves.hasNext())
//		{
//			ILeafNode n = leaves.next();
//			acceptor.addPosition(n.getOffset(), n.getLength(), DIRECTIVE);
//			
//			if (n.getText().equals("::"))
//				break;
//		}
//	}
	
	protected void highlight(ImageDirective obj, INode node, IHighlightedPositionAcceptor acceptor) {
		Iterator<ILeafNode> leaves = node.getLeafNodes().iterator();
		
		while(leaves.hasNext())
		{
			ILeafNode n = leaves.next();
			acceptor.addPosition(n.getOffset(), n.getLength(), DIRECTIVE);
			
			if (n.getText().equals("::"))
				break;
		}
	}
	
//	protected void highlight(BibDirective obj, INode node, IHighlightedPositionAcceptor acceptor) {
//		Iterator<ILeafNode> leaves = node.getLeafNodes().iterator();
//		
//		while(leaves.hasNext())
//		{
//			ILeafNode n = leaves.next();
//			acceptor.addPosition(n.getOffset(), n.getLength(), DIRECTIVE);
//			
//			if (n.getText().equals("::"))
//				break;
//		}
//	}
	
	protected void highlight(DirectiveOption obj, INode node, IHighlightedPositionAcceptor acceptor) {
//		Iterator<ILeafNode> leaves = node.getLeafNodes().iterator();
		Iterator<INode> leaves = node.getAsTreeIterable().iterator();
		while(leaves.hasNext())
		{
//			ILeafNode n = leaves.next();
			INode n = leaves.next();
			
			if (n.getGrammarElement() instanceof RuleCall)
			{
				String ruleName = ((RuleCall)n.getGrammarElement()).getRule().getName();
				
				if (ruleName.equals("SimpleText"))
					break;
				else if (ruleName.equals("DirectiveOption"))
					continue;
			}
			
			acceptor.addPosition(n.getOffset(), n.getLength(), DIRECTIVE);
		}
	}
	
	
	protected void highlight(Replacement obj, INode node, IHighlightedPositionAcceptor acceptor) {
		Iterator<ILeafNode> leaves = node.getLeafNodes().iterator();
		while(leaves.hasNext())
		{
			ILeafNode n = leaves.next();
			acceptor.addPosition(n.getOffset(), n.getLength(), DIRECTIVE);
			
			if (n.getText().equals("replace::"))
				break;
//			if (n.getGrammarElement() instanceof Keyword)
//			{
//				acceptor.addPosition(n.getOffset(), n.getLength(), DIRECTIVE);
//			}
		}
	}
	
	protected void highlight(ReplacementRef obj, INode node, IHighlightedPositionAcceptor acceptor) {
		acceptor.addPosition(node.getOffset(), node.getLength(), DIRECTIVE);
	}

	protected void highlight(Bold obj, INode node, IHighlightedPositionAcceptor acceptor) {
		acceptor.addPosition(node.getOffset(), node.getLength(), BOLD_TEXT);
	}
	
	protected void highlight(Italic obj, INode node, IHighlightedPositionAcceptor acceptor) {
		acceptor.addPosition(node.getOffset(), node.getLength(), ITALIC_TEXT);
	}
	
	protected void highlight(Heading obj, INode node, IHighlightedPositionAcceptor acceptor) {
		acceptor.addPosition(node.getOffset(), node.getLength(), HEADING);
	}
	
	protected void highlight(SimpleTextHeading obj, INode node, IHighlightedPositionAcceptor acceptor) {
		acceptor.addPosition(node.getOffset(), node.getLength(), HEADING);
	}
	
//    void setStyles(IHighlightedPositionAcceptor acceptor,
//            BidiIterator<INode> it, String... styles) {
//        for (String s : styles) {
//            if (!it.hasNext())
//                return;
//            INode n = skipWhiteSpace(acceptor, it);
//            if (n != null && s != null)
//                acceptor.addPosition(n.getOffset(), n.getLength(), s);
//        }
//    }
//
//    INode skipWhiteSpace(IHighlightedPositionAcceptor acceptor,
//            BidiIterator<INode> it) {
//        INode n = null;
//        while (it.hasNext()
//                && (n = it.next()).getClass() == HiddenLeafNode.class)
//            processHiddenNode(acceptor, (HiddenLeafNode) n);
//        return n;
//    }
//
//    INode skipWhiteSpaceBackwards(IHighlightedPositionAcceptor acceptor,
//            BidiIterator<INode> it) {
//        INode n = null;
//        while (it.hasPrevious()
//                && (n = it.previous()).getClass() == HiddenLeafNode.class)
//            processHiddenNode(acceptor, (HiddenLeafNode) n);
//        return n;
//    }
//
//    void processHiddenNode(IHighlightedPositionAcceptor acceptor,
//            HiddenLeafNode node) {
//        if (node.getGrammarElement() instanceof TerminalRuleImpl) {
//            TerminalRuleImpl ge = (TerminalRuleImpl) node.getGrammarElement();
//            if (ge.getName().equalsIgnoreCase("GUESS_COMMENT"))
//                acceptor.addPosition(node.getOffset(), node.getLength(),
//                        DIRECTIVE);
//        }
//
//    }

}