package rs.demsys.rst.ui.templates;

import org.eclipse.jface.text.templates.ContextTypeRegistry;
import org.eclipse.jface.text.templates.Template;
import org.eclipse.jface.text.templates.TemplateContext;
import org.eclipse.jface.text.templates.TemplateProposal;
import org.eclipse.jface.text.templates.persistence.TemplateStore;
import org.eclipse.xtext.ui.editor.contentassist.ContentAssistContext;
import org.eclipse.xtext.ui.editor.contentassist.ITemplateAcceptor;
import org.eclipse.xtext.ui.editor.templates.ContextTypeIdHelper;
import org.eclipse.xtext.ui.editor.templates.DefaultTemplateProposalProvider;

import rs.demsys.rst.services.RstGrammarAccess;

import com.google.inject.Inject;

public class RstTemplateProposalProvider extends
		DefaultTemplateProposalProvider {

	ContextTypeIdHelper helper;
	
	@Inject
	public RstTemplateProposalProvider(TemplateStore templateStore,
			ContextTypeRegistry registry, ContextTypeIdHelper helper) {
		super(templateStore, registry, helper);
		this.helper=helper;
	}

	@Inject
	RstGrammarAccess ga;
	
	@Override
	protected void createTemplates(TemplateContext templateContext,
			ContentAssistContext context, ITemplateAcceptor acceptor) {
		// "regular templates"
		super.createTemplates(templateContext, context, acceptor);

		createFigureTemplate(templateContext, context, acceptor);
		createNumfigTemplate(templateContext, context, acceptor);
		createCiteTemplate(templateContext, context, acceptor);
		createEqTemplate(templateContext, context, acceptor);
		createMathRoleTemplate(templateContext, context, acceptor);
		// add your own
	}
	
	protected void createNumfigTemplate(TemplateContext templateContext,
			ContentAssistContext context, ITemplateAcceptor acceptor) {
		
		String id=helper.getId(ga.getLiteralRule());
		
		if(templateContext.getContextType().getId().equals(id)){
			// create a template on the fly
			Template template = new Template(
					"num - Insert numbered figure reference",
					"Inserts new numbered figure reference into the document.",
					"numfigTemplateID",
					":num:`${Figure} #${ref:CrossReference(HashRef.Label)}`",
					true);// auto-insertable?
	
			// create a proposal
			TemplateProposal tp = createProposal(template, templateContext,
					context, getImage(template), getRelevance(template));
	
			// make it available
			acceptor.accept(tp);
		}
	}
	
	protected void createEqTemplate(TemplateContext templateContext,
			ContentAssistContext context, ITemplateAcceptor acceptor) {
		
		String id=helper.getId(ga.getLiteralRule());
		
		if(templateContext.getContextType().getId().equals(id)){
			// create a template on the fly
			Template template = new Template(
					"eq - Insert equation reference",
					"Inserts new equation reference into the document.",
					"eqTemplateID",
					":eq:`${ref:CrossReference(EqRole.ref)}`",
					true);// auto-insertable?
	
			// create a proposal
			TemplateProposal tp = createProposal(template, templateContext,
					context, getImage(template), getRelevance(template));
	
			// make it available
			acceptor.accept(tp);
		}
	}
	
	protected void createCiteTemplate(TemplateContext templateContext,
			ContentAssistContext context, ITemplateAcceptor acceptor) {
		
		String id=helper.getId(ga.getLiteralRule());
		
		if(templateContext.getContextType().getId().equals(id)){
			// create a template on the fly
			Template template = new Template(
					"cite - Insert citation reference",
					"Inserts new citation reference into the document.",
					"citeTemplateID",
					":cite:`${cursor}`",
					true);// auto-insertable?
	
			// create a proposal
			TemplateProposal tp = createProposal(template, templateContext,
					context, getImage(template), getRelevance(template));
	
			// make it available
			acceptor.accept(tp);
		}
	}
	
	protected void createMathRoleTemplate(TemplateContext templateContext,
			ContentAssistContext context, ITemplateAcceptor acceptor) {
		
		String id=helper.getId(ga.getLiteralRule());
		
		if(templateContext.getContextType().getId().equals(id)){
			// create a template on the fly
			Template template = new Template(
					"math - Insert math role",
					"Inserts new math role into the document.",
					"mathRoleTemplateID",
					":math:`${cursor}`",
					true);// auto-insertable?
	
			// create a proposal
			TemplateProposal tp = createProposal(template, templateContext,
					context, getImage(template), getRelevance(template));
	
			// make it available
			acceptor.accept(tp);
		}
	}
	
	protected void createFigureTemplate(TemplateContext templateContext,
			ContentAssistContext context, ITemplateAcceptor acceptor) {
		
		String id=helper.getId(ga.getSectionRule());
		
		if(templateContext.getContextType().getId().equals(id)){
			// create a template on the fly
			Template template = new Template(
					"fig - Insert new figure",
					"Inserts new figure into the document.",
					"figureTemplateID",
					".. _fig-${label}:\n" +
					"\n" +
					".. figure:: ${file_name}\n" +
					"    \n" +
					"    ${caption}\n",
					true);// auto-insertable?
	
			// create a proposal
			TemplateProposal tp = createProposal(template, templateContext,
					context, getImage(template), getRelevance(template));
	
			// make it available
			acceptor.accept(tp);
		}
	}

}
