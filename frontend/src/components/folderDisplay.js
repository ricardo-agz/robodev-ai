import { useState } from 'react';
import TreeView from '@mui/lab/TreeView';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import TreeItem from '@mui/lab/TreeItem';
import FolderIcon from '@mui/icons-material/Folder';
import JavascriptIcon from '@mui/icons-material/Javascript';
import axios from 'axios';
import { useRouter } from 'next/router';

export default function FolderDisplay({ buildfile }) {
    const router = useRouter()
    const [directory, setDirectory] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    useState(() => {
        let cancelled = false;
        if (!buildfile) {
            setError("no project data passed...");
            setLoading(false);
        }
        else {
            setLoading(true);
            axios.put(`${process.env.NEXT_PUBLIC_NEUTRINO_GENERATOR_URL}builddirectory`, buildfile)
                .then((r) => {
                    if (!cancelled) {
                        setDirectory(r.data);
                        setLoading(false);
                        setError(null);
                    }
                })
                .catch((err) => {
                    setLoading(false);
                    setError(err.response.data.message);
                });
    
            return () => {
                cancelled = true;
            };
        }

        
    }, []);

    const handleClickNode = (node) => {
        if (node.type === 'file') {
            router.push(`?page=${node.id}`);
        }
    };

    const renderTree = (nodes) => {
        return (
        <TreeItem
            key={nodes.id}
            nodeId={nodes.id}
            label={nodes.filename || nodes.name}
            onClick={() => handleClickNode(nodes)}
            endIcon={nodes.type === 'folder' ? <FolderIcon style={{ color: 'gray' }} /> : <JavascriptIcon />}
        >
            {Array.isArray(nodes.children)
                ? nodes.children.map((node) => renderTree(node))
                : null}
        </TreeItem>
    )};

    if (loading || !directory) {
        return <div>loading...</div>;
    }
    if (error) {
        return <div>error building project directory</div>;
    }
    return (
        <TreeView
            aria-label="rich object"
            defaultCollapseIcon={<ExpandMoreIcon/>}
            defaultExpanded={['server']}
            defaultExpandIcon={<ChevronRightIcon/>}
            sx={{
                flexGrow: 1, maxWidth: 400, overflowY: 'hidden', overflowX: 'hidden', color: 'white',
            }}
        >
            {renderTree(directory)}
        </TreeView>
    );
}
