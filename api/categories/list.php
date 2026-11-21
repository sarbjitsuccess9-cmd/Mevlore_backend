<?php
declare(strict_types=1);

require_once dirname(__DIR__, 2) . '/includes/db.php';
require_once dirname(__DIR__, 2) . '/includes/response.php';

MelvoreResponse::requireMethod('GET');

try {
    $pdo = MelvoreDB::pdo();
    $stmt = $pdo->query(
        "SELECT c.category_id, c.parent_id, c.name, c.slug, c.description, c.image,
                c.display_order, c.is_featured, COUNT(p.product_id) AS product_count
         FROM categories c
         LEFT JOIN products p ON p.category_id = c.category_id AND p.is_active = 1
         WHERE c.status = 'active'
         GROUP BY c.category_id
         ORDER BY c.display_order ASC, c.is_featured DESC, c.name ASC"
    );

    $categories = [];
    foreach ($stmt->fetchAll() as $row) {
        $categories[] = [
            'category_id' => (int)$row['category_id'],
            'parent_id' => $row['parent_id'] !== null ? (int)$row['parent_id'] : null,
            'name' => (string)$row['name'],
            'slug' => (string)$row['slug'],
            'description' => (string)($row['description'] ?? ''),
            'image_url' => MelvoreResponse::mediaUrl($row['image'] ?? null),
            'display_order' => (int)($row['display_order'] ?? 0),
            'is_featured' => ((int)($row['is_featured'] ?? 0)) === 1,
            'product_count' => (int)($row['product_count'] ?? 0),
        ];
    }

    MelvoreResponse::ok(['categories' => $categories], 'Categories loaded');
} catch (Throwable $e) {
    MelvoreResponse::error('Unable to load categories.', 'SERVER_ERROR', 500);
}
