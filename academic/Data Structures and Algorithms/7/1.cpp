#include <iostream>
#include <vector>
#include <string>
#include <windows.h>

/*

Деревья. Сортировка на двоичном дереве.
4, 5, 13, 8, 41, 52, 41, 64, 52, 17, 8, 9, 30
1) Реализуйте дерево в виде двусвязного списка
2) Обход слева, обход справа, симметрический обход.
3) Реализуйте программу сортировки массива на дереве методом симметрического обхода.

*/

struct Node {
    int key;
    Node* left;
    Node* right;
    Node* parent;

    Node(int val) : key(val), left(nullptr), right(nullptr), parent(nullptr) {}
};

class BinaryTree {
public:
    Node* root;

    BinaryTree() : root(nullptr) {}

    ~BinaryTree() {
        clear(root);
    }

    void clear(Node* node) {
        if (node) {
            clear(node->left);
            clear(node->right);
            delete node;
        }
    }

    void insert(int key) {
        Node* new_node = new Node(key);

        if (!root) {
            root = new_node;
            return;
        }

        Node* current = root;
        
        while (true) {
            if (key < current->key) {
                if (!current->left) {
                    current->left = new_node;
                    new_node->parent = current;
                    break;
                }
                current = current->left;
            } else {
                if (!current->right) {
                    current->right = new_node;
                    new_node->parent = current;
                    break;
                }
                current = current->right;
            }
        }
    }

    // Обход слева (Корень -> Левый -> Правый)
    void left_order(Node* node, std::vector<int>& result) {
        if (node) {
            result.push_back(node->key);
            left_order(node->left, result);
            left_order(node->right, result);
        }
    }

    // Обход справа (Левый -> Правый -> Корень)
    void right_order(Node* node, std::vector<int>& result) {
        if (node) {
            right_order(node->left, result);
            right_order(node->right, result);
            result.push_back(node->key);
        }
    }
     
    // Симметрический обход (Левый -> Корень -> Правый)
    void symmetric(Node* node, std::vector<int>& result) {
        if (node) {
            symmetric(node->left, result);
            result.push_back(node->key);
            symmetric(node->right, result);
        }
    }
    
    std::vector<int> init_tree_symmetric(const std::vector<int>& arr) {
        for (int val : arr) {
            insert(val);
        }

        std::vector<int> sorted_result;
        symmetric(root, sorted_result);
        return sorted_result;
    }

    void printVector(const std::string& label, const std::vector<int>& vec) {
        std::cout << label;
        for (int val : vec) {
            std::cout << val << " ";
        }
        std::cout << "\n";
    }
};

int main() {
    SetConsoleCP(65001);
    SetConsoleOutputCP(65001);
    
    std::vector<int> data = {4, 5, 13, 8, 41, 52, 41, 64, 52, 17, 8, 9, 30};

    BinaryTree tree;

    std::vector<int> sorted_data = tree.init_tree_symmetric(data);

    std::vector<int> left_res, right_res, sym_res;
    tree.left_order(tree.root, left_res);
    tree.right_order(tree.root, right_res);
    tree.symmetric(tree.root, sym_res);

    tree.printVector("Исходный массив:           ", data);
    tree.printVector("1. Обход слева (Pre-order): ", left_res);
    tree.printVector("2. Обход справа (Post-order):", right_res);
    tree.printVector("3. Симметрический (In-order): ", sym_res);

    return 0;
}