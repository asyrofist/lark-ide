from . import html5
from .examples import examples

from lark import Lark
from lark.tree import Tree


class App(html5.Div):
	def __init__(self):
		super().__init__("""
			<h1>
				<img src="lark-logo.png"> IDE
			</h1>
			
			<select [name]="examples">
				<option disabled selected>Examples</option>
			</select>
			<select [name]="parser">
				<option value="earley" selected>Earley (default)</option>
				<option value="lalr">LALR</option>
				<option value="cyk">CYK</option>
			</select>
			<textarea [name]="grammar" placeholder="Lark Grammar..."></textarea>
			<textarea [name]="input" placeholder="Parser input..."></textarea>
			<ul [name]="ast" />
		""")
		self.sinkEvent("onKeyUp", "onChange")

		self.parser = "earley"

		# Pre-load examples
		for name, (grammar, input) in examples.items():
			option = html5.Option(name)
			option.grammar = grammar
			option.input = input

			self.examples.appendChild(option)

	def onChange(self, e):
		if html5.utils.doesEventHitWidgetOrChildren(e, self.examples):
			example = self.examples.children(self.examples["selectedIndex"])
			self.grammar["value"] = example.grammar.strip()
			self.input["value"] = example.input.strip()
			self.onKeyUp()

		elif html5.utils.doesEventHitWidgetOrChildren(e, self.parser):
			self.parser = self.parser.children(self.parser["selectedIndex"])["value"]
			self.onKeyUp()

	def onKeyUp(self, e=None):
		l = Lark(self.grammar["value"], parser=self.parser)

		try:
			ast = l.parse(self.input["value"])
		except Exception as e:
			self.ast.appendChild(
				html5.Li(str(e)), replace=True
			)

		print(ast)
		traverse = lambda node: html5.Li([node.data, html5.Ul([traverse(c) for c in node.children])] if isinstance(node, Tree) else node)
		self.ast.appendChild(traverse(ast), replace=True)
