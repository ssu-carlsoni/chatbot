from typing import Any, Optional, List

from langchain.vectorstores import weaviate
from langchain_weaviate import WeaviateVectorStore as BaseWeaviateVectorStore
import weaviate


class WeaviateVectorStore(BaseWeaviateVectorStore):

    def delete(
            self,
            ids: Optional[List[str]] = None,
            tenant: Optional[str] = None,
            **kwargs: Any,
    ) -> None:
        if ids is None:
            fake_uuid = weaviate.util.generate_uuid5("NON_EXISTENT_ID")
            id_filter = weaviate.classes.query.Filter.by_id().not_equal(
                fake_uuid)
            with self._tenant_context(tenant) as collection:
                collection.data.delete_many(where=id_filter)
        else:
            super().delete(ids=ids, tenant=tenant, **kwargs)
