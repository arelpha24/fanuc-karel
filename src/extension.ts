import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
    context.subscriptions.push(
        vscode.languages.registerCompletionItemProvider('karel', {
            provideCompletionItems(document: vscode.TextDocument, position: vscode.Position) {
                // In a real extension, you might get these from a parsed document or web service.
                const functions = [
                    {
                        name: 'function1',
                        params: ['param1', 'param2']
                    },
                    {
                        name: 'function2',
                        params: ['paramA', 'paramB', 'paramC']
                    },
                    {
                        name: 'function3',
                        params: ['paramX']
                    }
                ];

                const completionItems = functions.map(func => {
                    const item = new vscode.CompletionItem(func.name, vscode.CompletionItemKind.Function);
                    item.insertText = func.name;

                    // Provide details about the function parameters.
                    item.detail = `(${func.params.join(', ')})`;
                    item.documentation = new vscode.MarkdownString(`**${func.name}**\n\nParameters:\n\n- ${func.params.join('\n- ')}`);

                    return item;
                });

                return completionItems;
            }
        }, '.')); // Trigger completion when '.' is pressed
}
